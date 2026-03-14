from datetime import timedelta

import yt_dlp
from flask import Blueprint, redirect, jsonify

_YDL_OPTS = {
    'format': 'bestaudio[ext=m4a]/bestaudio',
    'quiet': True,
    'no_warnings': True,
}


def get_video_info(video_id, action="location"):
    url = "https://www.youtube.com/watch?v=" + video_id
    with yt_dlp.YoutubeDL(_YDL_OPTS) as ydl:
        info = ydl.extract_info(url, download=False)

    duration = str(timedelta(seconds=info.get('duration', 0)))
    filesize = info.get('filesize') or info.get('filesize_approx') or 0

    if action == 'size':
        return {"id": video_id, "size": str(filesize), "duration": duration}
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
