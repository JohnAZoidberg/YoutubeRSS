import logging
import os

from flask import Blueprint, render_template, Response, request, jsonify, \
    abort

from .fetcher import Fetcher

logger = logging.getLogger(__name__)

home_page = Blueprint('home_page', __name__, template_folder='templates')


@home_page.errorhandler(LookupError)
def handle_not_found(e):
    return jsonify(error=str(e)), 404


@home_page.errorhandler(400)
def handle_bad_request(e):
    return jsonify(error=e.description), 400


def _get_limit():
    raw = request.args.get("limit")
    if raw is None:
        return None
    try:
        limit = int(raw)
    except ValueError:
        limit = 0
    if limit < 1:
        abort(400, description="limit must be a positive integer, got: %r"
              % raw)
    return limit


def serve(fetcher, podcast, playlist, limit):
    podcast["episodes"], newest_video = fetcher.get_videos(playlist, limit)

    xml = render_template(
        'basefeed.rss',
        # TODO sort the videos and get most recent date
        build_date=newest_video,
        podcast=podcast
    )
    return Response(xml, mimetype='text/xml')


def _get_fetcher():
    config_path = os.environ.get('YOUTUBERSS_CONFIG', 'conf.json')
    return Fetcher(config_path)


@home_page.route('/channel/<channelId>', methods=['GET'])
def serve_channel_podcast(channelId):
    limit = _get_limit()
    fetcher = _get_fetcher()
    podcast, upload_playlist = fetcher.get_channel_data(channelId)
    return serve(fetcher, podcast, upload_playlist, limit)


@home_page.route('/user/<username>', methods=['GET'])
def serve_user_podcast(username):
    limit = _get_limit()
    fetcher = _get_fetcher()
    podcast, upload_playlist = fetcher.get_user_data(username)
    return serve(fetcher, podcast, upload_playlist, limit)


@home_page.route('/list/<list_id>', methods=['GET'])
def serve_playlist_podcast(list_id):
    limit = _get_limit()
    fetcher = _get_fetcher()
    podcast, upload_playlist = fetcher.get_playlist_data(list_id)
    return serve(fetcher, podcast, upload_playlist, limit)
