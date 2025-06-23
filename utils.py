import logging
from datetime import datetime

# clear output file of any existing content
def refresh_output_file(limit: int, output_filepath: str) -> None:
    """
    Clears the output file and writes a header with the current timestamp.
    Args:
        limit (int): Number of top stories to include in the header.
        output_filepath (str): Path to the output file.
    """
    try:
        with open(output_filepath, "w") as output_file:
            output_file.write(f"Top {limit} HackerNews stories as of {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        logging.info("Output file cleared")
    except Exception as e:
        logging.error(f"Failed to refresh output file: {e}")

# update output file with post title, relevant url, and ChatGPT summary
def update_output_file(title: str, post_url: str, article_url: str, output_filepath: str, summary: str) -> None:
    """
    Appends a post's details and summary to the output file.
    Args:
        title (str): Title of the post.
        post_url (str): URL of the Hacker News post.
        article_url (str): URL of the article.
        output_filepath (str): Path to the output file.
        summary (str): Summary of the article.
    """
    try:
        with open(output_filepath, "a") as output_file:
            output_file.write(f"Title: {title}\nPost URL: {post_url}\nArticle URL: {article_url}\nSummary: {summary}\n\n")
        logging.info(f"Output file updated with post details")
    except Exception as e:
        logging.error(f"Failed to update output file: {e}")