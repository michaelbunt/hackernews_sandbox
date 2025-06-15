from pathlib import Path

TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
OUTPUT_FILEPATH = Path("output.txt")
MAX_STORIES = 3
SUMMARY_CHAR_LIMIT = 3000
POST_ENDPOINT = "https://hacker-news.firebaseio.com/v0/item/{post_id}.json"
POST_PERMALINK = "https://news.ycombinator.com/item?id={post_id}"
