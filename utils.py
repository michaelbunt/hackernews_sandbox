import logging
from datetime import datetime

# clear output file of any existing content
def refresh_output_file(limit, output_filepath):
    with open(output_filepath, "w") as output_file:
        output_file.write(f"Top {limit} HackerNews stories as of {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    logging.info("Output file cleared")

# update output file with post title, relevant url, and ChatGPT summary
def update_output_file(title, post_url, article_URL, output_filepath, summary):
    with open(output_filepath, "a") as output_file:
        output_file.write(f"Title: {title}\nPost URL: {post_url}\nArticle URL: {article_URL}\nSummary: {summary}\n\n")
    logging.info(f"Output file updated with post details")