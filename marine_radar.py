import os
import requests
from datetime import datetime, timedelta, timezone

# --- Telegram config from GitHub Secrets ---
TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def send_telegram(message: str):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    r = requests.post(url, data=payload)
    r.raise_for_status()


# --- iNaturalist config ---
BASE_URL = "https://api.inaturalist.org/v1/observations"

# Byron Bay lighthouse
LAT = -28.6474
LON = 153.6020
RADIUS_KM = 100

GROUPS = {
    "🐋 Whales & Dolphins": 152870,   # Cetacea
    "🦈 Sharks & Rays": 47273,       # Elasmobranchii
    "🐢 Sea Turtles": 39532,         # Testudines
}

def fetch_group_obs(taxon_id: int, d1: str, d2: str):
    params = {
        "lat": LAT,
        "lng": LON,
        "radius": RADIUS_KM,
        "taxon_id": taxon_id,
        "d1": d1,
        "d2": d2,
        "per_page": 200,
        "order": "desc",
        "order_by": "observed_on",
        "geo": "true",
        "verifiable": "true",
    }
    r = requests.get(BASE_URL, params=params)
    r.raise_for_status()
    return r.json().get("results", [])


def main():
    # 24h window
    now = datetime.now(timezone.utc)
    yesterday = now - timedelta(days=1)

    d1 = yesterday.date().isoformat()
    d2 = now.date().isoformat()

    summary = {}
    details = {}
    total_obs = 0

    # Fetch each group
    for name, taxon_id in GROUPS.items():
        obs = fetch_group_obs(taxon_id, d1, d2)
        summary[name] = len(obs)
        details[name] = obs
        total_obs += len(obs)

    # If nothing was observed — do nothing
    if total_obs == 0:
        print("No marine megafauna sightings. No Telegram alert sent.")
        return

    # Build message
    lines = []
    lines.append("🌊 Marine megafauna near Byron Bay")
    lines.append(f"Window: {d1} → {d2} (last 24h)")
    lines.append(f"Radius: {RADIUS_KM} km\n")

    # Summary
    for name, count in summary.items():
        lines.append(f"- {name}: {count} observations")

    lines.append("\n📘 Detailed sightings:")

    # Details (limit to 10)
    for group_name, obs_list in details.items():
        if not obs_list:
            continue

        lines.append(f"\n{group_name}:")
        for obs in obs_list[:10]:
            taxon = obs.get("taxon") or {}
            species = (
                taxon.get("preferred_common_name")
                or taxon.get("name")
                or "Unknown"
            )
            user = obs.get("user", {}).get("login", "unknown")
            date = obs.get("observed_on", "?")
            place = obs.get("place_guess", "Unknown location")
            lines.append(f"- {species} | @{user} | {date} | {place}")

    msg = "\n".join(lines)

    print(msg)
    send_telegram(msg)


if __name__ == "__main__":
    main()
