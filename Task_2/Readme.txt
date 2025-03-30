# MovieData Application

## Description
Fetches currently playing movies in Greece from TMDb and stores them in PostgreSQL.

## Requirements
- Python 3.x
- PostgreSQL
- Libraries: `requests`, `psycopg2` (install via `pip install requests psycopg2-binary`)

## Setup
1. Create a PostgreSQL database and run the provided DDL.
2. Update `DB_CONFIG` in `moviedata.py` with your DB credentials.
3. Run the script: `python moviedata.py`

## Features
- Fetches movies currently in theaters in Greece.
- Extracts title, description, original title, and directors.
- Stores IMDB links for directors.
- Updates the database on each run (no duplicates).

## Notes
- The script can be scheduled (e.g., via cron) for daily updates.
- No external TMDb libraries used—direct API calls only.