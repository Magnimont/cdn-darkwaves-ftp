import os
import re
import requests
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import TimedOut
from tenacity import retry, stop_after_attempt, wait_fixed

# Replace 'YOUR_BOT_TOKEN' with the token you received from the BotFather
BOT_TOKEN = '7295069840:AAHt42JOHNs4Ru9S34F-_chBBUOcDKFdvUg'
DOWNLOAD_DIR = 'downloads'  # Directory to save the downloaded files

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Send me a Telegram post link, and I will download the file for you.')

def download_file(url: str, local_filename: str) -> None:
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text
    if 't.me' in message:
        try:
            # Get the file from the Telegram post link
            file_url = extract_file_url_from_post(message)
            if file_url:
                local_filename = os.path.join(DOWNLOAD_DIR, file_url.split('/')[-1])
                download_file(file_url, local_filename)
                await update.message.reply_text(f'File downloaded successfully: {local_filename}')
            else:
                await update.message.reply_text('No file found in the provided link.')
        except Exception as e:
            await update.message.reply_text(f'Error: {e}')
    else:
        await update.message.reply_text('Please provide a valid Telegram post link.')

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def extract_file_url_from_post(post_link: str) -> str:
    try:
        # Extract chat ID and message ID from the post link
        match = re.match(r'https://t\.me/([^/]+)/(\d+)', post_link)
        if not match:
            raise ValueError('Invalid Telegram post link format.')

        username = match.group(1)
        print("username ", username)
        message_id = int(match.group(2))
        print("message_id ", message_id)

        bot = Bot(token=BOT_TOKEN)
        chat = bot.get_chat(username)
        print("chat ", chat)
        message = bot.get_chat(chat.id).message(message_id)  # Correct method for retrieving the message
        print("message ", message)

        # Check if the message contains any document or media
        if message.document:
            print("document")
            file_id = message.document.file_id
        elif message.photo:
            print("photo")
            file_id = message.photo[-1].file_id  # Get the highest resolution photo
        elif message.video:
            print("video")
            file_id = message.video.file_id
        else:
            raise ValueError('No downloadable file found in the provided link.')
        print("file_id ", file_id)

        file = bot.get_file(file_id)
        return file.file_path
    except Exception as e:
        print(f"Error extracting file URL from post: {e}")
        raise

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling(timeout=120, read_timeout=120)

if __name__ == '__main__':
    main()
