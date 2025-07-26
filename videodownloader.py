import os
import re
import threading
from dotenv import load_dotenv
from instaloader import Instaloader, Post

load_dotenv()
loader = Instaloader()

# Session file path
SESSION_FILE = f'{os.getcwd()}/session-{os.environ["INSTA_USER"]}'

session_lock = threading.Lock()

# Make a session file for the Instagram account
def load_or_create_session():
    with session_lock:
        if os.path.exists(SESSION_FILE):
            loader.load_session_from_file(
                os.environ["INSTA_USER"], filename=SESSION_FILE
            )
        else:
            loader.login(os.environ["INSTA_USER"], os.environ["INSTA_PASSWORD"])
            loader.save_session_to_file(SESSION_FILE)

# Load the session file
load_or_create_session()

# For instaloader exctract the shortcode from the url
def extract_shortcode(url, embeded_type):
    match = re.search(rf"{embeded_type}instagram\.com/(?:p|reel|tv)/([^/?#&]+)", url)
    return match.group(1) if match else None

# Get the video url media
def instagramDownload(url):
    try:
        reelPost = Post.from_shortcode(loader.context, extract_shortcode(url, "kk"))
        return reelPost.video_url if reelPost.is_video else reelPost.url
    except Exception as e:
        return "Error occured:" + str(e)
