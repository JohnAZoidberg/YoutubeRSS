#!/usr/bin/python
import urllib
import urllib2
import json
import sqlite3

import converter
import jinja_filters

#  YOU NEED TO CHANGE THIS TO YOUR ACTUAL API KEY
api_key = 'AIzaSyC-7Dy0KgpvvAK69BtdNJr5U2mJV2aN6Ew'
api_suffix = '&key=' + api_key
baseurl = 'https://www.googleapis.com/youtube/v3'
# YOU NEED TO CHANGE THIS TO THE FOLDER YOUR FILES ARE LOCATED IN
basefolder = 'http://youtuberss.danielschaefer.me/'
converturl = basefolder + 'converter/file/'


def build_url(request):
    return baseurl + request + api_suffix


def get_first_date(response):
    return jinja_filters.format_date_string(
        response['items'][0]['snippet']['publishedAt'])


def get_videos(playlistId):
    url = build_url('/playlistItems' +
                    '?part=snippet%2CcontentDetails' +
                    '&maxResults=50&playlistId=' + playlistId)
    vids = []
    next_page = ''
    while True:
        # We are limited to 50 results.
        # If the user subscribed to more than 50 channels
        # we have to make multiple requests here
        # which can only be fetched one after another.
        response = urllib2.urlopen(url + next_page).read()
        data = json.loads(response)
        vidsBatch = data['items']
        for vid in vidsBatch:
            vids.append(vid)
        try:  # loop until there are no more pages
            next_page = '&pageToken=' + data['nextPageToken']
        except KeyError:
            break
    return vids


def get_user_data(name):
    url = build_url('/channels?' +
                   'part=snippet%2CcontentDetails&forUsername=' + name)
    response = urllib.urlopen(url).read()
    itemJson = json.loads(response)
    channel = itemJson['items'][0]
    channelId = channel['id']

    podcast = {}
    podcast["url"] = 'https://www.youtube.com/user/' + name
    podcast["thumbnail"] = channel['snippet']['thumbnails']['high']['url']
    podcast["title"] = channel['snippet']['title']
    podcast["description"] = channel['snippet']['description']
    upload_playlist = \
        channel['contentDetails']['relatedPlaylists']['uploads']
    date = get_first_date(itemJson)
    return podcast, upload_playlist


def get_playlist_data(uploadPlaylist):
    url = build_url('/playlists?part=snippet&id=' + uploadPlaylist)
    response = urllib.urlopen(url).read()
    itemJson = json.loads(response)
    playlist = itemJson['items'][0]['snippet']

    podcast = {}
    podcast["url"] = 'https://www.youtube.com/playlist?list=' + \
        uploadPlaylist
    podcast["thumbnail"] = playlist['thumbnails']['high']['url']
    podcast["title"] = playlist['title']
    podcast["description"] = playlist['description']
    return podcast, uploadPlaylist


def get_video_information(upload_playlist):
    conn = sqlite3.connect('/home/zoid/videos.db')
    conn.execute('''
            CREATE TABLE IF NOT EXISTS videos
                (id       VARCHAR PRIMARY KEY NOT NULL,
                size     VARCHAR             NOT NULL,
                duration INT                 NOT NULL
            );''')
    conn.commit()
    vids = []
    for vid in get_videos(upload_playlist):
        video = {}
        snippet = vid['snippet']
        video["published_date"] = jinja_filters.format_date_string(snippet['publishedAt'])
        video["title"] = snippet['title']
        id = vid['snippet']['resourceId']['videoId']
        video["file_url"] = converturl + id
        video["description"] = snippet['description']
        video["url"] = 'https://www.youtube.com/watch?v=' + id

        # get size and duration
        try:
            info = get_cached_video_info(id, conn)
        except IOError:
            continue
        # cache this in an sqlite3 db
        video["length"] = info["size"]
        video["duration"] = info["duration"]
        vids.append(video)
    conn.commit()
    conn.close()
    return vids

def get_cached_video_info(video_id, conn):
        cur = conn.execute('''SELECT id, size, duration FROM videos
                              WHERE id = ?''', (video_id,))
        video = cur.fetchone()
        if video is None:
            info = converter.get_video_info(video_id, action="size")
            conn.execute(
                '''INSERT INTO videos (id, size, duration)
                   VALUES (?, ?, ?)'''
                , (video_id, info['size'], info["duration"])
            )
            return info
        else:
            return {"id": video_id, "size": video[1],
                    "duration": video[2]}
