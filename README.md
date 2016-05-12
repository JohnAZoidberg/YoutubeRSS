# YoutubeRSS
This little script returns a podcast compatible RSS feed for all videos of a YouTube channel or playlist.

## Usage
You just need to set the *api_key* variable to your YouTube API key and *basefolder* to the URL of the folder your files are in.
Just run it on a webserver and the RSS feed is available at:

    http://example.com/index.py?user=elliottsaidwhat
or

    http://example.com/index.py?playlist=UULrI-dOLyDbRnPyUeWadsOg

The script uses the other file to get the audio of the videos which you can manually use as well at:

    http://example.com/converter.py?v=dQw4w9WgXcQ

## Dependencies
This script was built for a CGI server but could easily modified for others as well.
- [pafy](https://github.com/mps-youtube/pafy)
- [lxml](https://github.com/lxml/lxml)
