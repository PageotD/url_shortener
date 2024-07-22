# shortener_app/main.py

"""
This module defines the main FastAPI application for the URL shortener service.

It includes endpoint definitions for:
- Root welcome message
- URL creation with validation
"""

import uvicorn
import validators
from fastapi import FastAPI, HTTPException
from . import schemas

app = FastAPI()

def raise_bad_request(message):
    """
    Raise an HTTP 400 Bad Request exception.

    Args:
        message (str): The error message to include in the exception.
    
    Raises:
        HTTPException: An exception with status code 400 and the provided message.
    """
    raise HTTPException(status_code=400, detail=message)

@app.get("/")
def read_root():
    """
    Handle GET requests to the root endpoint.

    Returns:
        str: A welcome message for the URL shortener API.
    """
    return "Welcome to the URL shortener API :)"

@app.post("/url")
def create_url(url: schemas.URLBase):
    """
    Handle POST requests to create a new shortened URL.

    Args:
        url (schemas.URLBase): The URL to be shortened, provided in the request body.
    
    Returns:
        str: A message indicating that the URL creation process is a TODO item.
    
    Raises:
        HTTPException: If the provided URL is not valid.
    """
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")
    return f"TODO: Create database entry for: {url.target_url}"

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
