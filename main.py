from scraper import scrape_all_venues
from spotify import find_artist, get_top_tracks, create_playlist
import random

MONTHS_AHEAD = 3  # How many months to generate
TRACKS_PER_ARTIST = 1

from datetime import datetime
from dateutil.relativedelta import relativedelta

current = datetime.now()

for i in range(MONTHS_AHEAD):
    target = current + relativedelta(months=i)
    month = target.month
    year = target.year
    month_name = target.strftime("%B")

    playlist_name = f"Bristol Live - {month_name} {year}"
    print(f"\n{'='*50}")
    print(f"Generating: {playlist_name}")
    print(f"{'='*50}")

    events = scrape_all_venues(month=month, year=year)

    all_artists = []
    for e in events:
        all_artists.extend(e["artists"])
    all_artists = list(set(all_artists))
    print(f"Found {len(all_artists)} unique artists")

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

    random.shuffle(all_track_uris)

    print(f"Found {len(found)} artists on Spotify")
    print(f"Could not find {len(not_found)} artists")
    print(f"Total tracks: {len(all_track_uris)}")

    if all_track_uris:
        print(f"Creating playlist '{playlist_name}'...")
        url = create_playlist(playlist_name, all_track_uris)
        print(f"Done! {url}")
    else:
        print("No tracks found, skipping playlist creation.")