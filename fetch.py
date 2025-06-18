import requests
import logging
from bs4 import BeautifulSoup
from config import TOP_STORIES_URL, SUMMARY_CHAR_LIMIT, POST_ENDPOINT

# retrieve post ids from hackernews top stories 
def fetch_post_ids(limit):
    try:
        response = requests.get(TOP_STORIES_URL)
        response.raise_for_status()
        return response.json()[:limit]
    except requests.exceptions.RequestException as e:
        logging.critical(f"Failed to fetch post ids: {e}")
        raise
    
    
# retrieve post details using post id
def fetch_post_details(post_id):
    try:
        response = requests.get(POST_ENDPOINT.format(post_id = post_id))
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Unable to get post details")
        return None

def fetch_article_text(article_url):
    try:
        response = requests.get(article_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = "\n".join(p.get_text() for p in paragraphs)
        return text.strip()[:SUMMARY_CHAR_LIMIT]
    except Exception as e:
        logging.error("Failed to fetch article content from article URL")
        return None
    
def fetch_post_metadata(post_ids: list[int]) -> list[dict]:
    metadata = []

    for post_id in post_ids:
        endpoint = POST_ENDPOINT.format(post_id=post_id)
        response = requests.get(endpoint)
        response.raise_for_status()
        data = response.json()

        try:
            metadata.append({
                "id" : post_id,
                "title" : data.get("title", "No Title"),
                "upvotes" : data.get("score", 0),
                "comments" : data.get("descendants", 0),
                "url" : data.get("url", "No URL")

            })
        except Exception as e:
            logging.warning(f"Skipping post due to error: {e}")
            continue

    return metadata