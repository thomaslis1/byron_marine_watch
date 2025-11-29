# 🌊 Byron Marine Watch

A tiny automation that checks iNaturalist for **whales, dolphins, sharks/rays, and sea turtles** near **Byron Bay** in the last 24 hours and sends a **Telegram message** if anything was seen.

---

## ✅ What It Does

- Looks for **verified, geotagged observations** on iNaturalist:
  - 🐋 Whales & dolphins (Cetacea)
  - 🦈 Sharks & rays (Elasmobranchii)
  - 🐢 Sea turtles (Testudines)
- Filters to a **100 km radius** around Byron Bay lighthouse.
- Summarises **counts per group** and lists up to **10 sightings per group**.
- **Only sends a Telegram message if at least one sighting** was recorded (no spam).

---

## ⚙️ How It Works

1. **`marine_radar.py`**
   - Calls the iNaturalist API for each taxon group.
   - Filters by:
     - Latitude/longitude (Byron Bay area)
     - Radius (100 km)
     - Date window (last 24 hours, by date)
     - `verifiable=true`, `geo=true`
   - Builds a summary message with emojis and basic sighting details.
   - Sends the message to a Telegram chat.

2. **GitHub Actions workflow**
   - Runs `marine_radar.py` once per day on GitHub’s servers.
   - Uses repository secrets for Telegram credentials.
   - If **no sightings**, the script exits silently (no Telegram message).

---

## 🧱 Tech Stack

- Python (`requests`, `datetime`)
- iNaturalist API
- Telegram Bot API
- GitHub Actions (cron-based workflow)

---

## 🚀 Setup

1. **Clone the repo** and add `marine_radar.py` at the project root.
2. Create a **Telegram bot** with [@BotFather](https://t.me/BotFather) and get:
   - Bot token
   - Your chat ID
3. In your GitHub repo, add these **Actions secrets**:
   - `TELEGRAM_TOKEN`
   - `TELEGRAM_CHAT_ID`
4. Add a GitHub Actions workflow that:
   - Checks out the repo
   - Sets up Python
   - Installs dependencies if needed
   - Runs `marine_radar.py` with `TELEGRAM_TOKEN` and `TELEGRAM_CHAT_ID` passed in as environment variables.
5. Adjust the cron schedule in the workflow if you want a different time of day.

---

## 🗺️ Current Config

- Location: **Byron Bay lighthouse** (lat/lon hardcoded in script)
- Radius: **100 km**
- Time window: **last 24 hours** (by date in UTC)
- Alert channel: **Telegram DM or group** (your chosen chat ID)

---
