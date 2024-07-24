"""
This module defines the main FastAPI application for the URL shortener service.

It includes endpoint definitions for:
- A root welcome message
- URL creation with validation and storage
"""

import uvicorn
import validators
import secrets

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.datastructures import URL

from . import crud, models, schemas
from .database import SessionLocal, engine
from .keygen import create_random_key
from .config import get_settings

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

def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    """
    Generate the administrative URL information for a given URL entry.

    This function takes a `models.URL` object, which represents a URL entry in the database,
    and constructs the administrative URL information by generating the full URL for accessing
    the URL's short and admin endpoints. It uses the base URL from the settings and the FastAPI
    application's URL path for the admin endpoint to create these URLs.

    Args:
        db_url (models.URL): An instance of `models.URL` representing the URL entry in the database.
            This object must include the `key` and `secret_key` attributes to construct the URLs.

    Returns:
        schemas.URLInfo: An instance of `schemas.URLInfo` with updated fields:
            - `url`: The full URL that redirects to the shortened URL based on the `key`.
            - `admin_url`: The full URL to access the administrative interface for this URL, based on the `secret_key`.

    Raises:
        Exception: Raises an exception if the URL or admin endpoint cannot be constructed properly.
    """
    base_url = URL(get_settings().base_url)
    admin_endpoint = app.url_path_for(
        "administration info", secret_key=db_url.secret_key
    )
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    return db_url


def raise_not_found(request):
    """
    Raise an HTTP 400 Bad Request exception with a custom message.

    Args:
        message (str): The error message to include in the exception.

    Raises:
        HTTPException: An exception with status code 404 and the provided message.
    """
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)

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

    db_url = crud.create_db_url(db=db, url=url)

    return get_admin_info(db_url)

@app.get("/{url_key}")
def forward_to_target_url(url_key: str, request: Request, db: Session = Depends(get_db)):
    """
    Forward to the target URL if the key is found and active in the database.
    
    Args:
        url_key (str): The key associated with the target URL.
        request (Request): The HTTP request object.
        db (Session): The database session.

    Returns:
        RedirectResponse: A response that redirects to the target URL.

    Raises:
        HTTPException: If the key is not found or inactive, raises a 404 Not Found error.
    """
    if db_url := crud.get_db_url_by_key(db=db, url_key=url_key):
        crud.update_db_clicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)

@app.get("/admin/{secret_key}", name="administration info", response_model=schemas.URLInfo)
def get_url_info(secret_key: str, request: Request, db: Session = Depends(get_db)):
    """
    Retrieve URL information based on the provided secret key.

    This endpoint allows for the retrieval of details about a URL stored in the database using its associated secret key.
    The response includes the shortened URL key and admin URL for the specified secret key.

    Args:
        secret_key (str): The secret key associated with the URL whose information is to be retrieved.
        request (Request): The HTTP request object, used here to provide the full URL for error messages.
        db (Session, optional): A SQLAlchemy database session obtained from the `get_db` dependency.

    Returns:
        schemas.URLInfo: The details of the URL including its shortened key and admin URL if found.

    Raises:
        HTTPException: If the URL with the given secret key is not found in the database,
                       raises a 404 Not Found error with a message indicating the URL does not exist.
    """
    if db_url := crud.get_db_url_by_secret_key(db, secret_key=secret_key):
        return get_admin_info(db_url)
    else:
        raise_not_found(request)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
