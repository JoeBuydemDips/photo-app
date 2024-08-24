import sys
import os
from pathlib import Path
import pytest
import httpx
from unittest.mock import MagicMock, patch

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Cyberpunk Photo Search" in response.text

@pytest.fixture
async def async_client():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_search_photos_success(async_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "results": [{"id": "1", "urls": {"small": "http://example.com/photo.jpg"}, "user": {"name": "Test User"}}],
        "total": 1,
        "total_pages": 1,
        "page": 1  # Include the page key in the mocked response
    }
    mock_response.headers = {"X-Total": "1", "X-Total-Pages": "1"}

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        async for client in async_client:
            response = await client.get("/search?query=test")
            assert response.status_code == 200
            data = response.json()
            assert "results" in data
            assert len(data["results"]) == 1
            assert data["total"] == 1
            assert "page" in data  # Ensure 'page' is in the response
            assert data["page"] == 1

@pytest.mark.asyncio
async def test_search_photos_api_error(async_client):
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError("API Error", request=MagicMock(), response=mock_response)
    mock_response.json.return_value = {"detail": "API Error"}
    mock_response.headers = {"X-Total": "1", "X-Total-Pages": "1"}
    with patch("httpx.AsyncClient.get", return_value=mock_response):
        async for client in async_client:
            response = await client.get("/search?query=test")
            assert response.status_code == 400
            assert "API Error" in response.json()["detail"]

@pytest.mark.asyncio
async def test_search_photos_pagination(async_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "results": [{"id": "1", "urls": {"small": "http://example.com/photo.jpg"}, "user": {"name": "Test User"}}],
        "total": 30,
        "total_pages": 3,
        "page": 2  # Include the page key in the mocked response
    }
    mock_response.headers = {"X-Total": "30", "X-Total-Pages": "3"}

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        async for client in async_client:
            response = await client.get("/search?query=test&page=2")
            assert response.status_code == 200
            data = response.json()
            assert "results" in data
            assert len(data["results"]) == 1
            assert data["total"] == 30
            assert "page" in data  # Ensure 'page' is in the response
            assert data["page"] == 2
            assert "total_pages" in data
            assert data["total_pages"] == 3

@pytest.mark.asyncio
async def test_search_photos_missing_api_key(async_client):
    with patch("app.main.os.getenv", return_value=None):
        async for client in async_client:
            response = await client.get("/search?query=test")
            assert response.status_code == 500
            assert response.json() == {"detail": "Unsplash API key not configured"}

@pytest.mark.asyncio
async def test_search_photos_empty_query(async_client):
    async for client in async_client:
        response = await client.get("/search?query=")
        assert response.status_code == 422
        assert "query" in response.json()["detail"][0]["loc"]

@pytest.mark.asyncio
async def test_search_photos_invalid_page(async_client):
    async for client in async_client:
        response = await client.get("/search?query=test&page=invalid")
        assert response.status_code == 422
        assert "page" in response.json()["detail"][0]["loc"]

@pytest.mark.asyncio
async def test_search_photos_negative_page(async_client):
    async for client in async_client:
        response = await client.get("/search?query=test&page=-1")
        assert response.status_code == 422
        assert "page" in response.json()["detail"][0]["loc"]

@pytest.mark.asyncio
async def test_search_photos_zero_page(async_client):
    async for client in async_client:
        response = await client.get("/search?query=test&page=0")
        assert response.status_code == 422
        assert "page" in response.json()["detail"][0]["loc"]

@pytest.mark.asyncio
async def test_search_photos_per_page(async_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "results": [{"id": "1", "urls": {"small": "http://example.com/photo.jpg"}, "user": {"name": "Test User"}}],
        "total": 1,
        "total_pages": 1
    }
    mock_response.headers = {"X-Total": "1", "X-Total-Pages": "1"}

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        async for client in async_client:
            response = await client.get("/search?query=test&per_page=15")
            assert response.status_code == 200
            data = response.json()
            assert "results" in data
            assert len(data["results"]) == 1  # Mocked response only has 1 result