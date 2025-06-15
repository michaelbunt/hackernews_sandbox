import tempfile
from utils import refresh_output_file, update_output_file

def test_refresh_output_file():
    with tempfile.NamedTemporaryFile(mode = "r+", delete=True) as temp_file:
        filepath = temp_file.name
        refresh_output_file(limit=2, output_filepath=filepath)

        temp_file.seek(0)
        content = temp_file.read()

        assert f"Top 2 HackerNews stories as of" in content
        assert len(content.strip().splitlines()) == 1

def test_update_output_file():
    # Step 1: Create a temporary file to simulate the output file
    with tempfile.NamedTemporaryFile(mode = "r+", delete=True) as temp_file:
        filepath = temp_file.name

        # Step 2: Create dummy data
        title = "Godzilla Attacks New York"
        post_url = "www.hackernews.com/postid_123456"
        article_url = "www.nypost.com/article7984"
        summary = "Godzilla strikes again, but this time on the East Coast of the United States"

        # Step 3: Call the function under test
        update_output_file(title, post_url, article_url, filepath, summary)

        # Step 4: Move cursor to beginning of file to read what was written
        temp_file.seek(0)
        content = temp_file.read()

        # Step 5: Verify content was added correct
        assert f"Title: {title}" in content
        assert f"Post URL: {post_url}" in content
        assert f"Article URL: {article_url}" in content
        assert f"Summary: {summary}" in content
