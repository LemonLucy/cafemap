# Venue - Cafe Finder

A Google Maps-style cafe discovery app with Starbucks-inspired design.

## Features
- 🗺️ Interactive Kakao Map with marker clustering
- ☕ Real-time cafe search based on map location
- 🎨 Category filtering (Work, Relax, Nature, Unique)
- 📋 Side panel with cafe details and photos
- 💼 Work cafes show outlets, WiFi speed, seating
- ✨ Unique cafes show themes and special menus

## Setup

1. Clone the repository
```bash
git clone <your-repo-url>
cd coffeemap
```

2. Set up frontend API key
```bash
cp config.example.js config.js
# Edit config.js and add your Kakao Maps JavaScript API key
```

3. Set up backend API keys
```bash
cp .env.example .env
# Edit .env and add your API keys
```

4. Run the server
```bash
# Option 1: Using the startup script (loads .env automatically)
./start.sh

# Option 2: Manual
export $(cat .env | grep -v '^#' | xargs)
python3 app_server.py
```

5. Open http://localhost:5000

## Getting Kakao API Key

1. Go to https://developers.kakao.com
2. Create an account and register your app
3. Go to [App Settings] > [Platform] > Add Web Platform
4. Register your domain (e.g., http://localhost:5000)
5. Copy the JavaScript key from the top of the page

## Tech Stack
- Frontend: HTML, CSS, JavaScript
- Map: Kakao Maps API
- Backend: Python (SimpleHTTPServer)
- Database: SQLite

## Project Structure
```
coffeemap/
├── index.html          # Main frontend UI
├── app_server.py       # Backend server (main)
├── database.py         # Database operations
├── config.js           # Frontend API key (not in git)
├── config.example.js   # Config template
├── .env                # Backend API keys (not in git)
├── .env.example        # Env template
├── start.sh            # Startup script
├── venue.db            # SQLite database (not in git)
└── README.md           # This file
```
