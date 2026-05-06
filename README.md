# Telegram Job Automator Bot

This bot allows users to send a job URL via Telegram, automatically extracts key information using AI, and appends it to a Google Sheet.

## How it Works
1. **URL Input**: User sends a URL (starting with `http://` or `https://`) to the Telegram bot.
2. **Scraping**: The bot scrapes the page content.
3. **AI Extraction**: An AI model extracts the company name, role, and deadline.
4. **Google Sheets Integration**: The extracted data is appended to a Google Sheet.

## Google Sheet Column Mapping
The bot updates the sheet with the following columns in order:
1. **Company**: Extracted company name.
2. **Program/Role**: Extracted role/title.
3. **Deadline**: Extracted deadline date.
4. **Applied?**: Defaulted to "No".
5. **Status**: Defaulted to "Pending".
6. **Job Description**: The original URL sent by the user.

## Setup
- Ensure `.env` contains:
  - `TELEGRAM_BOT_TOKEN`
  - `GOOGLE_SHEET_ID`
- Ensure `credentials.json` is present in the root directory.
- Install dependencies: `pip install -r requirements.txt`
- Run the bot: `python main.py`
