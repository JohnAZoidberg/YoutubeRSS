# YoutubeRSS

Convert any YouTube playlist or channel into a podcast RSS feed you can subscribe to with your favourite podcast player.

## Configuration

Create a `conf.json` in the project root (or set `YOUTUBERSS_CONFIG` to point elsewhere):

```json
{
    "api_key": "YOUR_YOUTUBE_API_KEY",
    "flask_root": "https://youtuberss.example.org/",
    "db_path": "local.db"
}
```

`db_path` points to a SQLite file used only as a cache for video sizes and
durations. It is safe to delete at any time and is flushed automatically
when the cache schema changes.

## Running

### With Nix

```bash
# Development shell with all dependencies
nix develop

# Run the app directly
nix run
```

### With pip

```bash
pip install -r requirements.txt
gunicorn --bind 0.0.0.0:8080 --workers 2 --timeout 120 wsgi:app
```

### With Docker

```bash
docker build -t youtuberss .
docker run -p 8080:8080 -v ./conf.json:/app/conf.json youtuberss
```

## Endpoints

- `/channel/<channel_id>?limit=50`
- `/user/<username>?limit=50`
- `/list/<playlist_id>?limit=50`

The `limit` query parameter limits the number of videos included in the feed. Useful for channels or playlists with thousands of videos.

You can also get the audio of a single video directly:

- `/converter/file/<video_id>` — redirects to the audio stream URL
