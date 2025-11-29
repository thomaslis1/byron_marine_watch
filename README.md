🌊 Byron Marine Watch

Daily marine-megafauna sightings around Byron Bay
Automatically tracks whales, dolphins, sharks, rays, and sea turtles reported on iNaturalist within 100 km of Byron Bay.
If anything is sighted in the last 24 hours, the bot sends a Telegram notification.

⸻

✅ What It Does
	•	Pulls recent iNaturalist observations for key marine groups:
	•	🐋 Whales & Dolphins
	•	🦈 Sharks & Rays
	•	🐢 Sea Turtles
	•	Filters sightings:
	•	Within 100 km of Byron Bay Lighthouse
	•	Reported in the last 24 hours
	•	Must be geotagged and verifiable
	•	Summarises totals
	•	Sends a formatted Telegram alert only if sightings exist
	•	Runs automatically once per day using GitHub Actions

⸻

📦 How It Works
	•	marine_radar.py
	•	Fetches observation data from the iNaturalist API
	•	Classifies sightings into groups
	•	Builds and sends a Telegram message
	•	.github/workflows/marine_radar.yml
	•	Runs daily at 08:00 UTC
	•	Calls the script on GitHub’s servers
	•	Uses GitHub Secrets for secure credentials
