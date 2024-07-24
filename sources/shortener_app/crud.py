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
