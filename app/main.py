from fastapi import FastAPI, Request, HTTPException
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
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/search")
async def search_photos(query: str, page: int = 1):
    logger.debug(f"Search query: {query}, Page: {page}")
    
    if not UNSPLASH_API_KEY:
        logger.error("Unsplash API key not found in environment variables")
        raise HTTPException(status_code=500, detail="Unsplash API key not configured")

    logger.debug(f"API Key: {UNSPLASH_API_KEY[:5]}...{UNSPLASH_API_KEY[-5:]}")

    headers = {"Authorization": f"Client-ID {UNSPLASH_API_KEY}"}
    params = {"query": query, "per_page": 30, "page": page}  # Fetch 30 photos per page

    logger.debug(f"Request headers: {headers}")
    logger.debug(f"Request params: {params}")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(UNSPLASH_API_URL, params=params, headers=headers)
            logger.debug(f"Response status code: {response.status_code}")
            logger.debug(f"Response headers: {response.headers}")
            
            response.raise_for_status()
            data = response.json()
            
            total_photos = int(response.headers.get('X-Total', 0))
            logger.info(f"Received {len(data.get('results', []))} results for query: {query}, Page: {page}, Total: {total_photos}")
            
            return {
                "results": data.get("results", []),
                "total": total_photos,
                "page": page
            }
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e}")
            logger.error(f"Response content: {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal server error")