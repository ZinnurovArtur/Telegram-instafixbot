import re
from instaloader import Instaloader, Post
import requests


loader = Instaloader()


def extract_shortcode(url):
    match = re.search(r"instagram\.com/(?:p|reel|tv)/([^/?#&]+)", url)
    return match.group(1) if match else None


def instagramDownload(url):
    try:
        reelPost = Post.from_shortcode(loader.context, extract_shortcode(url))
        print(reelPost)
        return reelPost.video_url if reelPost.is_video else reelPost.url
    except Exception as e:
        return "Error occured:" + str(e)
