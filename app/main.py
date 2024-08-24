from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
import httpx
import logging

# Load environment variables
load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

UNSPLASH_API_KEY = os.getenv("UNSPLASH_API_KEY")
UNSPLASH_API_URL = "https://api.unsplash.com/search/photos"

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request})

@app.get("/search")
async def search_photos(
    query: str = Query(..., min_length=1),
    page: int = Query(1, gt=0),
    per_page: int = Query(10, gt=0, le=30)
):
    api_key = os.getenv("UNSPLASH_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Unsplash API key not configured")

    url = f"https://api.unsplash.com/search/photos"
    params = {
        "query": query,
        "page": page,
        "per_page": per_page,
        "client_id": api_key
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return {
                "results": data["results"],
                "total": int(response.headers.get("X-Total", 0)),
                "page": page,  # Include the page key in the response
                "total_pages": int(response.headers.get("X-Total-Pages", 0))
            }
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")