import logging
from datetime import timedelta

import yt_dlp
from flask import Blueprint, redirect, jsonify

logger = logging.getLogger(__name__)

_YDL_OPTS = {
    'format': 'bestaudio[ext=m4a]/bestaudio/best',
    'quiet': True,
    'no_warnings': True,
}


def get_video_info(video_id, action="location"):
    url = "https://www.youtube.com/watch?v=" + video_id
    with yt_dlp.YoutubeDL(_YDL_OPTS) as ydl:
        info = ydl.extract_info(url, download=False)

    duration = str(timedelta(seconds=info.get('duration', 0)))
    filesize = info.get('filesize') or info.get('filesize_approx') or 0

    logger.debug("Video %s: duration=%s filesize=%s", video_id, duration, filesize)

    if action == 'size':
        # A size taken from a video+audio fallback format (e.g. when YouTube
        # temporarily withholds audio-only streams) should not be cached as
        # authoritative, so report which kind of format it came from.
        audio_only = info.get('vcodec') in (None, 'none')
        return {"id": video_id, "size": str(filesize), "duration": duration,
                "audio_only": audio_only}
    else:
        return info['url']


converter_page = Blueprint('converter_page', __name__,
                           template_folder='templates')


@converter_page.route('/converter/file/<video_id>', methods=['GET'])
def get_file(video_id):
    # TODO handle empty video_id
    url = get_video_info(video_id, action="location")
    return redirect(url)


@converter_page.route('/converter/size/<video_id>', methods=['GET'])
def get_size(video_id):
    # TODO handle empty video_id
    return jsonify(get_video_info(video_id, action="size"))
