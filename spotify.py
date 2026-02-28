import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import random

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope="playlist-modify-public"
))

def find_artist(name):
    results = sp.search(q=name, type="artist", limit=1)
    artists = results["artists"]["items"]
    if not artists:
        return None
    # Basic check - name should roughly match
    top = artists[0]
    if top["name"].lower() in name.lower() or name.lower() in top["name"].lower():
        return top
    return None

def get_top_tracks(artist_id, n=1):
    try:
        results = sp.artist_albums(artist_id, album_type="album,single", limit=3)
        albums = results["items"]
        if not albums:
            return []
        # Just get the first track from the most recent release
        first_album = albums[0]
        tracks = sp.album_tracks(first_album["id"], limit=1)
        if not tracks["items"]:
            return []
        return [tracks["items"][0]["uri"]]
    except Exception as e:
        print(f"    Error getting tracks: {e}")
        return []

def create_playlist(name, track_uris):
    user_id = sp.me()["id"]
    playlist = sp.user_playlist_create(user_id, name, public=True)
    # Spotify allows max 100 tracks per request
    for i in range(0, len(track_uris), 100):
        sp.playlist_add_items(playlist["id"], track_uris[i:i+100])
    return playlist["external_urls"]["spotify"]

# Test - just check we can connect
user = sp.me()
print(f"Connected as: {user['display_name']}")