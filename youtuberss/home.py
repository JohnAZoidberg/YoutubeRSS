#!/usr/bin/python -u
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")

from datetime import datetime

from flask import Blueprint, render_template, jsonify, Response

import fetcher
import jinja_filters

home_page = Blueprint('home_page', __name__, template_folder='templates')


@home_page.route('/user/<username>', methods=['GET'])
def serve_channel_podcast(username):
    podcast, upload_playlist = fetcher.get_user_data(username)
    podcast["episodes"] = fetcher.get_video_information(upload_playlist)

    return render_template(
        'basefeed.rss',
        # TODO sort the videos and get most recent date
        build_date=jinja_filters.format_date(datetime.now()),
        podcast=podcast
    )


@home_page.route('/list/<list_id>', methods=['GET'])
def serve_playlist_podcast(list_id):
    podcast = {}
    podcast["url"] = "http://example.com"
    podcast["thumbnail"] = "thumbnail"
    podcast["title"] = "this is the title"
    podcast["publish_date"] = '2016-04-27T11:09:12.000Z'
    podcast["description"] = 'this text describes this podcast episode'
    podcast, upload_playlist = fetcher.get_playlist_data(list_id)
    vids = fetcher.get_video_information(upload_playlist)
    podcast["episodes"] = vids

    xml = render_template(
        'basefeed.rss',
        # TODO sort the videos and get most recent date
        build_date=jinja_filters.format_date(datetime.now()),
        podcast=podcast
    )
    return Response(xml, mimetype='text/xml')
