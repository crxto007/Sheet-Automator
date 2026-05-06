import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from telegram.request import HTTPXRequest

from scraper import scrape_url
from ai_extractor import extract_job_info
from sheets import append_job_row

load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    
    if not url.startswith(("http://", "https://")):
        await update.message.reply_text("Please send a valid URL starting with http:// or https://")
        return

    await update.message.reply_text("Processing URL... please wait a moment ⏳")

    # 1. Scrape the URL
    text = scrape_url(url)
    if not text:
        await update.message.reply_text("Sorry, I couldn't scrape the page. It might be protected or the link is broken.")
        return

    # 2. Extract information using AI
    job_data = extract_job_info(text)
    if not job_data:
        await update.message.reply_text("AI failed to extract job information from this page.")
        return

    # 3. Append to Google Sheets
    # Format: [Company, Program/Role, Deadline, Applied?, Status, Job Description]
    row = [
        job_data.get("company_name", "Unknown"),
        job_data.get("program_role", "Unknown"),
        job_data.get("deadline", "Not found"),
        "No",
        "Pending",
        url
    ]
    
    try:
        append_job_row(row)
        confirmation = (
            f"✅ Added to sheet!\n\n"
            f"🏢 *Company*: {row[0]}\n"
            f"🎓 *Role*: {row[1]}\n"
            f"📅 *Deadline*: {row[2]}\n"
            f"🔗 *URL*: {row[5]}"
        )
        await update.message.reply_text(confirmation, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Sheet error: {e}")
        await update.message.reply_text("Extracted info, but I had trouble updating the Google Sheet.")

def run_bot():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    # Increase timeout to 30 seconds to avoid ConnectTimeout/ReadTimeout
    request = HTTPXRequest(connect_timeout=30, read_timeout=30)
    app = ApplicationBuilder().token(token).request(request).build()

    # Handle any text message that looks like a URL
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot is running...")
    app.run_polling()
