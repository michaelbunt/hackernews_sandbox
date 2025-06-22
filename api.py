import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from apscheduler.schedulers.background import BackgroundScheduler

from db import fetch_latest, insert_row
from fetch import fetch_post_ids, fetch_post_metadata, fetch_article_text
from summarize import summarize_text
from agent import SummarizerAgent

# Create scheduler instance
scheduler = BackgroundScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    scheduler.add_job(fetch_and_store, "interval", minutes=3, args=[30, 3])
    scheduler.start()
    print("Scheduler started")
    
    # Run once immediately
    fetch_and_store(30, 3)
    
    yield
    
    # Shutdown
    scheduler.shutdown()
    print("Scheduler stopped")

app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="templates")

# Return the latest n summaries as JSON.
# http://127.0.0.1:8000/summaries

@app.get("/summaries")
def get_summaries(limit: int = 10):
    rows = fetch_latest(limit)
    return [
        {
            "id":         r[0],
            "title":      r[1],
            "points":     r[2],
            "comments":   r[3],
            "summary":    r[4],
            "created_at": r[5],
        }
        for r in rows
    ]

# Render an HTML page listing the latest summaries.
# http://127.0.0.1:8000

@app.get("/", response_class=HTMLResponse)
def html_report(request: Request, limit: int = 10):
    rows = fetch_latest(limit)
    posts = [
        {
            "id":         r[0],
            "title":      r[1],
            "points":     r[2],
            "comments":   r[3],
            "summary":    r[4],
            "created_at": r[5],
        }
        for r in rows
    ]
    return templates.TemplateResponse("report.html", {"request": request, "posts": posts})

def fetch_and_store(number_candidates, number_selected):
    print('Executing scheduled post(s) fetch')
    ids = fetch_post_ids(number_candidates)
    candidate_metadata = fetch_post_metadata(ids)
    
    agent = SummarizerAgent()
    metadata = agent.choose_posts_with_llm(candidate_metadata, number_selected)

    for post in metadata:
        article_text = fetch_article_text(post["url"])
        input_text = article_text if article_text else post["title"]
        summary = summarize_text(input_text)
        post["summary"] = summary
        insert_row(post)

# Remove the old scheduler setup lines that were at the bottom