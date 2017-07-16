#!/usr/bin/python -u
# coding=utf-8
import datetime

from flask import Blueprint, render_template, jsonify, Response, request

from . import fetcher
from . import jinja_filters

home_page = Blueprint('home_page', __name__, template_folder='templates')

@home_page.route('/', methods=['GET'])
def home():
    return """
    Welcome!<br>
    At /list/<playlistid> you can find the feed of a playlist.<br>
    At /user/<username> you can find the feed of this user.
    """

@home_page.route('/user/<username>', methods=['GET'])
def serve_channel_podcast(username):
    limit = request.args.get("limit")
    podcast, upload_playlist = fetcher.get_user_data(username)
    podcast["episodes"], newest_video = fetcher.get_videos(upload_playlist, limit)

    xml = render_template(
        'basefeed.rss',
        # TODO sort the videos and get most recent date
        build_date=newest_video,
        podcast=podcast
    )
    return Response(xml, mimetype='text/xml')


@home_page.route('/list/<list_id>', methods=['GET'])
def serve_playlist_podcast(list_id):
    limit = request.args.get("limit")
    podcast, upload_playlist = fetcher.get_playlist_data(list_id)
    podcast["episodes"], newest_video = fetcher.get_videos(upload_playlist, limit)

    xml = render_template(
        'basefeed.rss',
        # TODO sort the videos and get most recent date
        build_date=newest_video,
        podcast=podcast
    )
    return Response(xml, mimetype='text/xml')
