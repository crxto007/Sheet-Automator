from bot import run_bot

if __name__ == "__main__":
    try:
        run_bot()
    except Exception as e:
        print(f"Critical error starting the bot: {e}")
