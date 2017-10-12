import datetime


def format_date(date):
    return date.strftime("%a, %d %b %Y %H:%M:%S GMT")


def youtube_to_date(youtubeString):
    # youtube '2016-04-27T11:09:12.000Z'
    # desired 'Mon, 25 Apr 2016 19:03:00 GMT'

    dateSplit = youtubeString.split('-')
    if not dateSplit:
        return youtubeString
    year = dateSplit[0]
    month = dateSplit[1]
    (day, times) = dateSplit[2].split('T')
    timeSplit = times.split(':')
    hour = timeSplit[0]
    minutes = timeSplit[1]
    (seconds, timezone) = timeSplit[2].split('.')
    date = datetime.datetime(int(year), int(month), int(day),
                             int(hour), int(minutes), int(seconds))
    return date


def format_date_string(youtubeString):
    return format_date(youtube_to_date(youtubeString))


def shorten(long_string):
    return long_string[:80]


def cdata(content):
    return "<![CDATA[%s]]>" % content
