#main.py
import openai
import os
import logging
import argparse
from datetime import datetime
from config import POST_PERMALINK
from fetch import fetch_post_details, fetch_post_ids, fetch_article_text
from summarize import summarize_text
from utils import refresh_output_file, update_output_file

def parse_args():
    parser = argparse.ArgumentParser(description = "Summarize top HackerNews posts")
    parser.add_argument("--posts", type=int, default=3, help="Number of top posts to summarize")
    parser.add_argument("--output", type=str, default="output.txt", help="File path to output file containing summaries")
    parser.add_argument("--level", type=str, default="INFO", help="Log level")
    return parser.parse_args()

args=parse_args()

logger = logging.getLogger()

log_level = getattr(logging, args.level.upper(), logging.INFO)
logger.setLevel(log_level)

console_handler = logging.StreamHandler()

log_filename = f"logs/run_{datetime.now().strftime('%m%d%Y_%H%M%S')}.log"
file_handler = logging.FileHandler(log_filename, "w")

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

def setup_openai_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logging.critical("Open AI API Key Not found - confirm configuration details")
        raise ValueError("Open AI API Key Not found")
    openai.api_key = api_key
    logging.info("OpenAI API ready")

def main(args):
    refresh_output_file(args.posts, args.output)
    top_post_ids = fetch_post_ids(args.posts)

    for post_id in top_post_ids:
        logging.info(f"-----Processing post id: {post_id}-----")
        post_url = f"{POST_PERMALINK.format(post_id = post_id)}"
        logging.info(f"Hackernews URL: {post_url}")
    
        post_details = fetch_post_details(post_id)
        if not post_details:
            logging.error(f"Unable to retrieve post details for post id: {post_id}")
            continue
        
        title = post_details.get("title", "No title found")
        logging.info(f"Title: '{title}'...")

        article_url = post_details.get("url", "N/A")
        logging.info(f"Article URL: {article_url}")

        article_text = fetch_article_text(article_url)
        if article_text:
            input_text = article_text
        else: 
            input_text = f"{title}\n{post_url}"
        
        summary = summarize_text(input_text)
        if not summary:
            logging.error(f"Unable to retrieve post summary for post id: {post_id}")
            continue
        logging.info(f"Summary: {summary}")

        update_output_file(title, post_url, article_url, args.output, summary)

if __name__ == "__main__":
    args = parse_args()
    setup_openai_key()
    logging.info(f"""
        CLI Args:
        Number of Posts = {args.posts},
        Outoput Filepath = {args.output},
        Log Level = {args.level}
""")
    main(args)