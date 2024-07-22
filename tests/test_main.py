# shortener_app/test_main.py

import pytest
from fastapi.testclient import TestClient
from shortener_app.main import app

# Create a TestClient instance for testing the FastAPI app
client = TestClient(app)

def test_read_root():
    """
    Test the root endpoint ("/") of the FastAPI application.
    """
    # Send a GET request to the root endpoint
    response = client.get("/")
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Assert that the response JSON content is the expected welcome message
    assert response.json() == "Welcome to the URL shortener API :)"
