#!/usr/bin/python -u
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")

import datetime

from flask import Blueprint, render_template, jsonify, Response, request

from fetcher import Fetcher
import jinja_filters

home_page = Blueprint('home_page', __name__, template_folder='templates')


def serve(fetcher, podcast, playlist, limit):
    podcast["episodes"], newest_video = fetcher.get_videos(playlist, limit)

    xml = render_template(
        'basefeed.rss',
        # TODO sort the videos and get most recent date
        build_date=newest_video,
        podcast=podcast
    )
    return Response(xml, mimetype='text/xml')


@home_page.route('/channel/<channelId>', methods=['GET'])
def serve_channel_podcast(channelId):
    limit = request.args.get("limit")
    fetcher = Fetcher(request.environ['YOUTUBERSS_CONFIG'])
    podcast, upload_playlist = fetcher.get_channel_data(channelId)
    return serve(fetcher, podcast, upload_playlist, limit)


@home_page.route('/user/<username>', methods=['GET'])
def serve_user_podcast(username):
    limit = request.args.get("limit")
    fetcher = Fetcher(request.environ['YOUTUBERSS_CONFIG'])
    print "What the fuck is going on here"
    print request.environ['YOUTUBERSS_CONFIG']
    podcast, upload_playlist = fetcher.get_user_data(username)
    return serve(fetcher, podcast, upload_playlist, limit)


@home_page.route('/list/<list_id>', methods=['GET'])
def serve_playlist_podcast(list_id):
    limit = request.args.get("limit")
    fetcher = Fetcher(request.environ['YOUTUBERSS_CONFIG'])
    podcast, upload_playlist = fetcher.get_playlist_data(list_id)
    return serve(fetcher, podcast, upload_playlist, limit)
