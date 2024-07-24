import secrets
import string
from sqlalchemy.orm import Session
from . import crud

def create_random_key(length: int = 5) -> str:
    """
    Generate a random key of specified length.

    Parameters:
    length (int): The length of the key to be generated. Default is 5.

    Returns:
    str: A string containing the randomly generated key.
    """
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))

def create_unique_random_key(db: Session) -> str:
    key = create_random_key()
    while crud.get_db_url_by_key(db, key):
        key = create_random_key()
    return key
