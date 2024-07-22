"""
This module defines the Pydantic models for the URL shortener application.

These models are used for data validation and serialization.
"""

from pydantic import BaseModel

class URLBase(BaseModel):
    """
    Represents the base model for a URL with the target URL.

    Attributes:
        target_url (str): The original URL that will be shortened.
    """
    target_url: str

class URL(URLBase):
    """
    Represents the detailed model for a URL including additional information.

    Inherits from URLBase and adds more attributes.

    Attributes:
        is_active (bool): Indicates if the shortened URL is active.
        clicks (int): The number of times the shortened URL has been clicked.
    """
    is_active: bool
    clicks: int

    class Config:
        """
        Configuration class for Pydantic model to enable ORM mode.

        orm_mode allows the model to be used with ORM objects.
        """
        orm_mode = True

class URLInfo(URL):
    """
    Represents the complete model for a URL including administrative information.

    Inherits from URL and adds administrative URLs.

    Attributes:
        url (str): The shortened URL.
        admin_url (str): The administrative URL for managing the shortened URL.
    """
    url: str
    admin_url: str
