import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

BASE = "https://www.headfirstbristol.co.uk"

VENUES = [
    "exchange", "the-fleece", "thekla", "the-louisiana", "bristol-beacon",
    "o2-academy", "strange-brew", "the-croft", "rough-trade-bristol",
    "the-trinity-centre", "motion", "lakota", "mr-wolfs", "the-canteen",
    "jam-jar", "the-gallimaufry", "the-stag-and-hounds", "the-thunderbolt",
    "old-market-assembly", "the-grain-barge", "loco-klub", "losthorizon",
    "cafe-kino", "the-bristol-fringe", "the-love-inn", "the-mount-without",
    "st-georges-hall", "watershed"
]

MONTH_MAP = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12
}

def parse_date_from_slug(slug):
    match = re.search(r'(mon|tue|wed|thu|fri|sat|sun)-(\d{1,2})-([a-z]{3})', slug)
    if match:
        day = int(match.group(2))
        month = MONTH_MAP.get(match.group(3))
        year = datetime.now().year
        if month and month < datetime.now().month:
            year += 1
        return f"{year}-{month:02d}-{day:02d}" if month else None
    return None

def scrape_venue(venue_slug):
    url = f"{BASE}/whats-on/{venue_slug}"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if r.status_code != 200:
        print(f"  Skipping {venue_slug} ({r.status_code})")
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    events = []
    seen = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]

        # Match full URLs for this venue's events
        prefix = f"{BASE}/whats-on/{venue_slug}/"
        if not href.startswith(prefix):
            continue

        event_slug = href.replace(prefix, "")
        if event_slug in seen:
            continue
        seen.add(event_slug)

        title = a.text.strip()
        title = re.sub(r'\s*(in Bristol|at .+)?\s*(Tickets|tickets)?\s*$', '', title).strip()

        date = parse_date_from_slug(event_slug)

        events.append({
            "title": title,
            "venue": venue_slug,
            "date": date,
            "url": href
        })

    return events

def scrape_all_venues(month, year):
    all_events = []
    for venue in VENUES:
        print(f"Scraping {venue}...")
        events = scrape_venue(venue)
        for e in events:
            if e["date"] and e["date"].startswith(f"{year}-{month:02d}"):
                all_events.append(e)
    return all_events

events = scrape_all_venues(month=3, year=2026)
for e in events:
    print(e["date"], "-", e["venue"], "-", e["title"])

print(f"\nTotal events found: {len(events)}")