#!/usr/bin/python
import json
import sqlite3

import requests

import converter

BASEURL = 'https://www.googleapis.com/youtube/v3'

# TODO prevent from running to long and fetch only 50 more than are in the DB
class Fetcher:
    def __init__(self, config_file):
        with open(config_file) as f:
            config = json.load(f)

        api_key = config["api_key"]
        basefolder = config["flask_root"]
        self.database_path = config["db_path"]

        self.api_suffix = '&key=' + api_key
        self.converturl = basefolder + 'converter/file/'
        pass

    def _build_url(self, request):
        return BASEURL + request + self.api_suffix

    def _extract_video_info(self, vid, conn):
        video = {}
        snippet = vid['snippet']
        video["published_date"] = snippet['publishedAt']
        video["title"] = snippet['title']
        video["id"] = vid['snippet']['resourceId']['videoId']
        video["file_url"] = self.converturl + video["id"]
        video["description"] = snippet['description']
        video["url"] = 'https://www.youtube.com/watch?v=' + video["id"]

        # get size and duration
        info = self._get_cached_video_info(video["id"], conn)
        video["length"] = info["size"]
        video["duration"] = info["duration"]
        return video


    def get_data(self, url):
        itemJson = requests.get(url).json()
        channel = itemJson['items'][0]

        podcast = {}
        podcast["url"] = 'https://www.youtube.com/channel/' + channel['id']
        podcast["thumbnail"] = channel['snippet']['thumbnails']['high']['url']
        podcast["title"] = channel['snippet']['title']
        podcast["description"] = channel['snippet']['description']
        upload_playlist = \
            channel['contentDetails']['relatedPlaylists']['uploads']
        return podcast, upload_playlist


    def get_channel_data(self, channelId):
        url = self._build_url('/channels?' +
                         'part=snippet%2CcontentDetails&id=' + channelId)
        return self.get_data(url)

    def get_user_data(self, name):
        url = self._build_url('/channels?' +
                         'part=snippet%2CcontentDetails&forUsername=' + name)
        return self.get_data(url)


    def get_playlist_data(self, uploadPlaylist):
        url = self._build_url('/playlists?part=snippet&id=' + uploadPlaylist)
        itemJson = requests.get(url).json()
        playlist = itemJson['items'][0]['snippet']

        podcast = {}
        podcast["url"] = 'https://www.youtube.com/playlist?list=' + \
            uploadPlaylist
        podcast["thumbnail"] = playlist['thumbnails']['high']['url']
        podcast["title"] = playlist['title']
        podcast["description"] = playlist['description']
        return podcast, uploadPlaylist


    def get_videos(self, playlist_id, limit=None):
        conn = sqlite3.connect(self.database_path)
        conn.execute('''
                CREATE TABLE IF NOT EXISTS videos
                    (id       VARCHAR PRIMARY KEY NOT NULL,
                    size     VARCHAR             NOT NULL,
                    duration INT                 NOT NULL
                );''')
        conn.commit()
        url = self._build_url('/playlistItems' +
                         '?part=snippet%2CcontentDetails' +
                         '&maxResults=50&playlistId=' + playlist_id)
        vids = []
        newest_date = None
        next_page = ''
        counter = 0
        limit = None if limit is None else int(limit)
        while (limit is None or counter < limit):
            # We are limited to 50 results.
            # If the user subscribed to more than 50 channels
            # we have to make multiple requests here
            # which can only be fetched one after another.
            data = requests.get(url + next_page).json()
            vidsBatch = data['items']
            for vid in vidsBatch:
                try:
                    print "VideoId: ", vid['snippet']['resourceId']['videoId']
                    video = self._extract_video_info(vid, conn)
                except IOError:
                    continue
                except:
                    print "VideoId: ", vid['snippet']['resourceId']['videoId']
                    conn.commit()
                    continue
                    # raise
                print "VideoId: ", vid['snippet']['resourceId']['videoId']
                vids.append(video)
                if newest_date is None:
                    newest_date = video['published_date']
                elif video['published_date'] > newest_date:
                        newest_date = video['published_date']
                counter += 1
                if limit is not None and counter >= limit:
                    break
            try:  # loop until there are no more pages
                next_page = '&pageToken=' + data['nextPageToken']
            except KeyError:
                break
        conn.commit()
        conn.close()
        return vids, newest_date


    def _get_cached_video_info(self, video_id, conn):
            cur = conn.execute('''SELECT id, size, duration FROM videos
                                  WHERE id = ?''', (video_id,))
            video = cur.fetchone()
            if video is None:
                info = converter.get_video_info(video_id, action="size")
                conn.execute(
                    '''INSERT INTO videos (id, size, duration)
                       VALUES (?, ?, ?)''',
                    (video_id, info['size'], info["duration"])
                )
                return info
            else:
                return {"id": video_id, "size": video[1],
                        "duration": video[2]}
