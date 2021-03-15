import logging
import os

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from facebook_scraper import get_posts

TOKEN = os.getenv('RAM_TOKEN')
CHANNEL = os.getenv('RAM_CHANNEL')
CHECK_INTERVAL = 180

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

last_post_id = 0


def check_posts(context: CallbackContext) -> None:
    global last_post_id
    bot = context.bot
    posts = list(get_posts('Tervetuloameille', pages=1))
    post = posts[0]
    post_id = int(post['post_id'])
    if last_post_id == post_id:
        return
    last_post_id = post_id
    photo = post['image']
    post_text = post['post_text'] or ''
    bot.sendPhoto(chat_id='@{}'.format(CHANNEL), photo=photo, caption=post_text)


def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    updater.start_polling()
    updater.job_queue.run_repeating(check_posts, CHECK_INTERVAL, 1)

    updater.idle()


if __name__ == '__main__':
    if not TOKEN:
        print("missing token")
        exit(1)

    if not CHANNEL:
        print("missing channel")
        exit(1)

    main()
