#!/usr/bin/python
import cgitb
import cgi
import pafy

cgitb.enable()
form = cgi.FieldStorage()

baseurl = "https://www.youtube.com/watch?v="
id = form.getvalue('v')
action = form.getvalue('action')
url = baseurl + id
video = pafy.new(url)
for s in video.audiostreams:
    if s.extension == 'm4a':
        if action == 'size':
            print 'Content-type:text/html\r\n\r\n'
            print '{"id": "' + id + '", "size": "' + str(s.get_filesize()) + '"}'
        else:
            print "Location:", s.url
            print
