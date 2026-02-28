from scraper import scrape_all_venues
from spotify import find_artist, get_top_tracks, create_playlist
import random

MONTH = 3
YEAR = 2026
PLAYLIST_NAME = f"Bristol Gigs - March 2026"
TRACKS_PER_ARTIST = 1

print("Scraping Headfirst Bristol...")
events = scrape_all_venues(month=MONTH, year=YEAR)

# Get unique artists
all_artists = []
for e in events:
    all_artists.extend(e["artists"])
all_artists = list(set(all_artists))
print(f"Found {len(all_artists)} unique artists")

# Find each artist on Spotify and get tracks
print("\nSearching Spotify...")
all_track_uris = []
found = []
not_found = []

for artist_name in all_artists:
    artist = find_artist(artist_name)
    if artist:
        tracks = get_top_tracks(artist["id"], n=TRACKS_PER_ARTIST)
        if tracks:
            all_track_uris.extend(tracks)
            found.append(artist_name)
            print(f"  ✓ {artist_name}")
    else:
        not_found.append(artist_name)
        print(f"  ✗ {artist_name}")

# Shuffle the playlist
random.shuffle(all_track_uris)

print(f"\nFound {len(found)} artists on Spotify")
print(f"Could not find {len(not_found)} artists")
print(f"Total tracks: {len(all_track_uris)}")

# Create the playlist
if all_track_uris:
    print(f"\nCreating playlist '{PLAYLIST_NAME}'...")
    url = create_playlist(PLAYLIST_NAME, all_track_uris)
    print(f"Done! Playlist URL: {url}")