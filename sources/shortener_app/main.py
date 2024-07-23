"""
This module defines the main FastAPI application for the URL shortener service.

It includes endpoint definitions for:
- A root welcome message
- URL creation with validation and storage
"""

import uvicorn
import validators
import secrets

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine

app = FastAPI()

# Create all tables defined in the models
models.Base.metadata.create_all(bind=engine)

def get_db():
    """
    Dependency function to provide a database session.

    This function is used as a dependency in route handlers to obtain
    a database session, which is automatically closed after the request
    is completed.

    Yields:
        Session: A SQLAlchemy session object.

    Finally:
        Closes the session to free up resources.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def raise_bad_request(message):
    """
    Raise an HTTP 400 Bad Request exception with a custom message.

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

@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    """
    Handle POST requests to create a new shortened URL.

    Validates the provided URL, generates a unique short key and secret key,
    and stores the URL along with these keys in the database.

    Args:
        url (schemas.URLBase): The URL to be shortened, provided in the request body.
        db (Session, optional): A SQLAlchemy database session obtained from the `get_db` dependency.

    Returns:
        schemas.URLInfo: The details of the created URL including its short and admin URLs.

    Raises:
        HTTPException: If the provided URL is not valid.
    """
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")

    # Generate random keys for URL shortening
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = "".join(secrets.choice(chars) for _ in range(5))
    secret_key = "".join(secrets.choice(chars) for _ in range(8))
    
    # Create a new URL entry in the database
    db_url = models.URL(
        target_url=url.target_url,
        key=key,
        secret_key=secret_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    
    # Set URL and admin URL for response
    db_url.url = key
    db_url.admin_url = secret_key

    return db_url

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
