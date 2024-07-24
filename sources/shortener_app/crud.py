# shortener_app/crud.py

from sqlalchemy.orm import Session
from . import keygen, models, schemas

def create_db_url(db: Session, url: schemas.URLBase) -> models.URL:
    """
    Create a new URL entry in the database with a random key and secret key.

    Parameters:
    db (Session): The SQLAlchemy database session.
    url (schemas.URLBase): The URL schema object containing the target URL.

    Returns:
    models.URL: The newly created URL entry in the database.
    """
    key = keygen.create_random_key()
    secret_key = keygen.create_random_key(length=8)
    db_url = models.URL(
        target_url=url.target_url, key=key, secret_key=secret_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_db_url_by_key(db: Session, url_key: str) -> models.URL:
    """
    Retrieve a URL entry from the database by its key.

    Parameters:
    db (Session): The SQLAlchemy database session.
    url_key (str): The key of the URL entry to retrieve.

    Returns:
    models.URL: The URL entry if found and active, otherwise None.
    """
    return (
        db.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active)
        .first()
    )

def get_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL:
    """
    Retrieve a URL entry from the database by its secret key.

    Parameters:
    db (Session): The SQLAlchemy database session.
    secret_key (str): The admin secret_key of the URL entry to retrieve.

    Returns:
    models.URL: The URL entry if found and active, otherwise None.
    """
    return (
        db.query(models.URL)
        .filter(models.URL.secret_key == secret_key, models.URL.is_active)
        .first()
    )

def update_db_clicks(db: Session, db_url: schemas.URL) -> models.URL:
    """
    Increment the click count for a given URL entry in the database.

    This function updates the `clicks` attribute of a `schemas.URL` object, which represents
    a URL entry in the database. It increments the click count by one, commits the changes
    to the database, and refreshes the object to ensure the most recent state is returned.

    Args:
        db (Session): A SQLAlchemy `Session` object used to interact with the database.
        db_url (schemas.URL): An instance of `schemas.URL` representing the URL entry to be updated.
            This object must include the `clicks` attribute, which will be incremented.

    Returns:
        models.URL: The updated `models.URL` object reflecting the incremented click count and
            the most recent state after committing the changes to the database.

    Raises:
        Exception: Raises an exception if there are issues with committing changes to the database
            or refreshing the object. This could include issues related to database connectivity
            or transaction management.
    """
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url

def deactivate_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL:
    """
    Deactivates a URL entry in the database by setting its `is_active` status to `False`.

    This function retrieves a URL entry from the database using the provided secret key. If the URL entry is found,
    it sets the `is_active` attribute to `False`, commits the change to the database, and then refreshes the URL object.

    Args:
        db (Session): The SQLAlchemy database session to be used for querying and committing changes.
        secret_key (str): The secret key associated with the URL entry to be deactivated.

    Returns:
        models.URL: The URL object that was deactivated. If the URL with the given secret key does not exist, `None` is returned.

    Raises:
        Exception: If the URL entry cannot be found with the provided secret key.
    """
    db_url = get_db_url_by_secret_key(db, secret_key)

    if db_url:
        db_url.is_active = False
        db.commit()
        db.refresh(db_url)

    return db_url

