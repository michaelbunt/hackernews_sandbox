from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from db import fetch_latest

app = FastAPI()

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
