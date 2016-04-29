#!/usr/bin/python
import cgitb
import cgi
import urllib
import urllib2
import json
from podcastFeed import PodcastFeed
import datetime

cgitb.enable()
form = cgi.FieldStorage()
api_key = 'AIzaSyC-7Dy0KgpvvAK69BtdNJr5U2mJV2aN6Ew'
api_suffix = '&key=' + api_key
baseurl = 'https://www.googleapis.com/youtube/v3'
converturl = 'http://pi.jzoid.xyz/youtuberss/converter_raspbian.py?v='

print "Content-Type: text/xml;charset=utf-8"
print
print '<?xml version="1.0" encoding="UTF-8" ?>'

def buildUrl(request):
    return baseurl + request + api_suffix

def youtubeToMp3(youtubeId):
    baseurl = converturl + youtubeId
    return ("1", baseurl)

def formatDate(date):
    return date.strftime("%a, %d %b %Y %H:%M:%S GMT")

def formatDateString(youtubeDate):
    #youtube '2016-04-27T11:09:12.000Z'
    #desired 'Mon, 25 Apr 2016 19:03:00 GMT'

    dateSplit = youtubeDate.split('-')
    year = dateSplit[0]
    month = dateSplit[1]
    (day, times) = dateSplit[2].split('T')
    timeSplit = times.split(':')
    hour = timeSplit[0]
    minutes = timeSplit[1]
    (seconds, timezone) = timeSplit[2].split('.')
    date = datetime.datetime(int(year), int(month), int(day), int(hour), int(minutes), int(seconds))
    return formatDate(date)

def getFirstDate(response):
    return formatDateString(response['items'][0]['snippet']['publishedAt'])

def getVideos(playlistId):
    url = buildUrl('/playlistItems?part=snippet&maxResults=50&playlistId=' + playlistId)
    vids = []
    next_page = ''
    while True:
        # We are limited to 50 results. If the user subscribed to more than 50 channels
        # we have to make multiple requests here which can only be fetched one after another.
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

name = form.getfirst('user')
url = buildUrl('/channels?forUsername=' + name + '&part=snippet%2CcontentDetails')
response = urllib.urlopen(url).read()
itemJson = json.loads(response)
channel = itemJson['items'][0]
#print response
id = channel['id']
thumbnail = channel['snippet']['thumbnails']['high']['url']
description = channel['snippet']['description']
title = channel['snippet']['title']
uploadPlaylist = channel['contentDetails']['relatedPlaylists']['uploads']

email = 'shop@theschooloflife.com'
date = getFirstDate(itemJson)
rss = PodcastFeed(
    title=title,
    desc=description,
    lng='en-us',
    copyright=title + " " + datetime.date.today().strftime("%Y"),
    link='http://pi.danielschaefer.me/youtuberss/index_raspbian.py?user=' + name,
    lastBuildDate=formatDate(datetime.date.today()),#date,#'Mon, 25 Apr 2016 23:03:00 GMT', # TODO sort the videos and get most recent date
    image=thumbnail,
    category='News & Politics', # TODO check if it is optional and leave it out or get it from the video
    channelName=name
)

for vid in getVideos(uploadPlaylist):
    snippet = vid['snippet']
    date = formatDateString(snippet['publishedAt'])
    title = snippet['title']
    id = vid['snippet']['resourceId']['videoId']
    size, url = youtubeToMp3(id)
    if url is None:
        continue
    description = snippet['description']

    rss.addItem(
        title=title,
        link=url,
        size=size,
        desc=description,
        pubDate=date#'Mon, 25 Apr 2016 19:03:00 GMT'
    )

print rss.to_string()