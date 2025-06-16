#main.py
import openai
import os
import logging
import argparse
from datetime import datetime
from config import POST_PERMALINK
from fetch import fetch_post_details, fetch_post_ids, fetch_article_text, fetch_post_metadata
from summarize import summarize_text
from utils import refresh_output_file, update_output_file

def parse_args():
    parser = argparse.ArgumentParser(description = "Summarize top HackerNews posts")
    parser.add_argument("--posts", type=int, default=3, help="Number of top posts to summarize")
    parser.add_argument("--output", type=str, default="output.txt", help="File path to output file containing summaries")
    parser.add_argument("--level", type=str, default="INFO", help="Log level")
    return parser.parse_args()

args=parse_args()

def setup_logging(args):
    logger = logging.getLogger()
    log_level = getattr(logging, args.level.upper(), logging.INFO)
    logger.setLevel(log_level)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(f"logs/run_{datetime.now().strftime('%m%d%Y_%H%M%S')}.log", "w")

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
    metadata = fetch_post_metadata(top_post_ids)

    for post in metadata:
        post_id = post["id"]
        title = post["title"]
        post_url = f"{POST_PERMALINK.format(post_id = post_id)}"
        article_url = post["url"]

        logging.info(f"----- Processing post id: {post_id} -----")
        logging.info(f"Hackernews URL: {post_url}")
        logging.info(f"Title: '{title}'")
        logging.info(f"Article URL: {article_url}'")

        article_text = fetch_article_text(article_url)
        input_text = article_text if article_text else f"{title}\n{post_url}"
        
        summary = summarize_text(input_text)
        if not summary:
            logging.error(f"Unable to retrieve post summary for post id: {post_id}")
            continue
        
        logging.info(f"Summary: {summary}")
        update_output_file(title, post_url, article_url, args.output, summary)

if __name__ == "__main__":
    args = parse_args()
    setup_logging(args)
    setup_openai_key()
    logging.info(f"CLI Args: posts = {args.posts}, output = {args.output}, level = {args.level}")
    main(args)