# YoutubeRSS
With this program you can convert any Youtube playlist or channel to a podcast RSS feed that you can subscribe to with your favourite RSS player.

## Running
You can run this service in multiple different ways:

- For debuggin run `youtuberss/__init__.py` directly
- Use a WSGI server to run the `youtuberss` module
- Use Docker and build from the `Dockerfile`
- The recommended deployment (how I use it) however it to use my [NixOS module](https://github.com/JohnAZoidberg/nix-konfiguriert/blob/master/daniel/modules/youtuberss.nix)

Additionally you need to create a configuration file `conf.json` in the root directory of the project with the following content:

```json
{
    "api_key": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "flask_root": "https://youtuberss.example.org",
    "db_path": "local.db"
}
```

## Endpoints
- `/users/<user_id>?limit=50`
- `/channel/<channel_id>?limit=50`
- `/playlist/<playlist_id>?limit=50`

As you can see the query parameter `limit` can limit the number of videos that
are included in the feed.  This is particularly useful for channels or
playlists with thousands of videos.  The Youtube API limits us to fetch 50
videos at once and makes it impossible to parallelize this task.
