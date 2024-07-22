# shortener_app/test_schemas.py

import pytest
from pydantic import ValidationError
from shortener_app.schemas import URLBase, URL, URLInfo

def test_url_base():
    """
    Test the URLBase model with valid and invalid data.
    """
    # Valid data
    url_base = URLBase(target_url="https://example.com")
    assert url_base.target_url == "https://example.com"

def test_url():
    """
    Test the URL model with valid and invalid data.
    """
    # Valid data
    url = URL(target_url="https://example.com", is_active=True, clicks=10)
    assert url.target_url == "https://example.com"
    assert url.is_active is True
    assert url.clicks == 10

    # Invalid data: clicks should be an int
    with pytest.raises(ValidationError):
        URL(target_url="https://example.com", is_active=True, clicks="ten")

def test_url_info():
    """
    Test the URLInfo model with valid and invalid data.
    """
    # Valid data
    url_info = URLInfo(
        target_url="https://example.com",
        is_active=True,
        clicks=10,
        url="http://short.url/abcd",
        admin_url="http://short.url/admin/abcd"
    )
    assert url_info.target_url == "https://example.com"
    assert url_info.is_active is True
    assert url_info.clicks == 10
    assert url_info.url == "http://short.url/abcd"
    assert url_info.admin_url == "http://short.url/admin/abcd"

if __name__ == "__main__":
    pytest.main()
