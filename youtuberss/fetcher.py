#!/usr/bin/python
import cgitb
import cgi
import urllib
import urllib2
import json
import datetime

import jinja_filters

cgitb.enable()
form = cgi.FieldStorage()
#  YOU NEED TO CHANGE THIS TO YOUR ACTUAL API KEY
api_key = 'AIzaSyC-7Dy0KgpvvAK69BtdNJr5U2mJV2aN6Ew'
api_suffix = '&key=' + api_key
baseurl = 'https://www.googleapis.com/youtube/v3'
# YOU NEED TO CHANGE THIS TO THE FOLDER YOUR FILES ARE LOCATED IN
basefolder = 'http://youtuberss.danielschaefer.me/'
converturl = basefolder + 'converter.py?v='


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
    podcast["publish_date"] = "" # WHAT AM I GONNA PUT HERE?
    podcast["description "] = channel['snippet']['description']
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
    podcast["publish_date"] = "" # WHAT AM I GONNA PUT HERE?
    podcast["description"] = playlist['description']
    return podcast, uploadPlaylist


def get_video_information(upload_playlist):
    vids = []
    for vid in get_videos(upload_playlist):
        video = {}
        snippet = vid['snippet']
        video["published_date"] = jinja_filters.format_date_string(snippet['publishedAt'])
        video["title"] = snippet['title']
        id = vid['snippet']['resourceId']['videoId']
        video["file_url"] = converturl + id
        video["description"] = snippet['description']
        video["url"] = 'https://www.youtube.com/watch?v=' + id,
        vids.append(video)
    return vids
