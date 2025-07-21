#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to  convert the Instagram reels link to embeded link for telegram or discord

Usage:
Send instagram reel link and bot reply you with embeded video or photo
"""

import logging
import mimetypes
import os
import random
import re
import time
from urllib import response
from dotenv import load_dotenv

import requests
from telegram import ForceReply, Update
import telegram
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from videodownloader import instagramDownload

load_dotenv()
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

bot_last_message = {}


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def sendInsta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if bot_last_message:
        bot_last_message.clear()
    raw_text = update.message.text
    filtered_insta = re.sub(
        r"^https://www\.instagram\.com/", os.environ["SERVER_URL"], raw_text
    )
    sent = await update.message.reply_text(filtered_insta)
    time.sleep(random.random() * 2 + 3.0)
    bot_last_message[update.effective_chat.id] = sent
    messageObject = next(iter(bot_last_message.values()))

    if not messageObject.link_preview_options:
        await update.message.reply_chat_action(telegram.constants.ChatAction.TYPING)
        progress_message = await update.message.reply_text("Trying new server...⏳")
        time.sleep(random.random() * 2 + 3.0)

        edited_message = await editMessage(messageObject, context)
        time.sleep(random.random() * 2 + 3.0)
        if (
            not edited_message.link_preview_options
            or edited_message.link_preview_options.is_disabled
        ):
            await progress_message.edit_text("Okay I will download video...⏳")
            time.sleep(random.random() * 2 + 3.0)
            media_post = instagramDownload(edited_message.text)

            await send_converted_insta_file(media_post, context,edited_message)

        await progress_message.delete()

    return


async def send_converted_insta_file(media_post, context, edited_message):
    if not media_post:
        return
    file_name = f"temp_file.mp4" if "mp4" in media_post else "temp_file.jpg"

    try:
        response = requests.get(media_post, stream=True)
        response.raise_for_status()
        with open(file_name, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
            with open(file_name, "rb") as converted_file:
                if "mp4" in media_post:
                    await context.bot.send_video(
                        chat_id=edited_message.chat_id, video=converted_file
                    )
                else:
                    await context.bot.send_photo(
                        chat_id=edited_message.chat_id, photo=converted_file
                    )

    except Exception as e:
        logger.error(f"Error converting media:{e}")
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)


async def editMessage(messageObject, context: ContextTypes.DEFAULT_TYPE):
    newUrl = re.sub(
        rf'{os.environ["SERVER_URL"]}', os.environ["SERVER_URL2"], messageObject.text
    )
    return await context.bot.edit_message_text(
        chat_id=messageObject.chat.id, message_id=messageObject.id, text=newUrl
    )


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.environ["TELEGRAM_TOKEN"]).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(
        MessageHandler(
            filters.TEXT
            & filters.Regex(r"^https://www\.instagram\.com/")
            & (filters.Entity("url") | filters.Entity("text_link")),
            sendInsta,
        )
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
