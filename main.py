import logging
import os

from telegram.ext import Updater, CallbackContext
from facebook_scraper import get_posts

TOKEN = os.getenv('RAM_TOKEN')
CHANNEL = os.getenv('RAM_CHANNEL')
PAGES = ['Tervetuloameille', 'sanojaelamasta', 'pienia.sanoja']
CHECK_INTERVAL = 180

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

last_post_ids = {p: 0 for p in PAGES}


def check_posts_for_page(page: str):
    posts = list(get_posts(page, pages=1))

    try:
        post = posts[0]
        post_id = int(post['post_id'])

        if last_post_ids[page] == post_id:
            return None

        last_post_ids[page] = post_id
        photo = post['image']
        # telegram only accepts 200 characters at maximum
        post_text = post['post_text'][:200] or ''

        return (photo, post_text)
    except:
        return None


def check_posts(context: CallbackContext) -> None:
    bot = context.bot
    for page in PAGES:
        post = check_posts_for_page(page)
        if post:
            bot.sendPhoto(chat_id='@{}'.format(CHANNEL),
                          photo=post[0], caption=post[1])


def main() -> None:
    updater = Updater(TOKEN)

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
