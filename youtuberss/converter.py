#!/usr/bin/python
import pafy
from flask import Blueprint, redirect


def get_video_info(video_id, action="location"):
    baseurl = "https://www.youtube.com/watch?v="
    url = baseurl + video_id
    video = pafy.new(url)
    #print video.duration
    #print video.length
    for s in video.audiostreams:
        if s.extension == 'm4a':
            if action == 'size':
                return '{"id": "%s", "size": "%s"}' \
                       .format(video_id, str(s.get_filesize()))
            else:
                return s.url


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
    return get_video_info(video_id, action="size")
