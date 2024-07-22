# shortener_app/test_main.py

import pytest
from fastapi.testclient import TestClient
from shortener_app.main import app, raise_bad_request

# Create a TestClient instance for testing the FastAPI app
client = TestClient(app)

def test_read_root():
    """
    Test the root endpoint ("/") of the FastAPI application.

    This function sends a GET request to the root endpoint and checks:
    - The response status code is 200 (OK).
    - The response JSON content matches the expected welcome message.
    """
    # Send a GET request to the root endpoint
    response = client.get("/")
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Assert that the response JSON content is the expected welcome message
    assert response.json() == "Welcome to the URL shortener API :)"

def test_create_url_valid():
    """
    Test the URL creation endpoint ("/url") with a valid URL.

    This function sends a POST request with a valid URL and checks:
    - The response status code is 200 (OK).
    - The response content contains the expected TODO message.
    """
    # Send a POST request with valid URL data
    response = client.post("/url", json={"target_url": "https://example.com"})
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Assert that the response content contains the expected TODO message
    assert response.json() == "TODO: Create database entry for: https://example.com"

def test_create_url_invalid():
    """
    Test the URL creation endpoint ("/url") with an invalid URL.

    This function sends a POST request with an invalid URL and checks:
    - The response status code is 400 (Bad Request).
    - The response detail contains the expected error message.
    """
    # Send a POST request with invalid URL data
    response = client.post("/url", json={"target_url": "invalid-url"})
    
    # Assert that the response status code is 400 (Bad Request)
    assert response.status_code == 400
    
    # Assert that the response detail contains the expected error message
    assert response.json() == {"detail": "Your provided URL is not valid"}

def test_raise_bad_request():
    """
    Test the raise_bad_request function.

    This function calls raise_bad_request and checks:
    - An HTTPException is raised with the expected status code and detail message.
    """
    with pytest.raises(Exception) as excinfo:
        raise_bad_request("Test error message")
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Test error message"

if __name__ == "__main__":
    pytest.main()