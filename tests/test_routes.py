"""Tests for root endpoint"""


def test_root_redirect_to_index(client):
    """
    Test the root endpoint redirects to /static/index.html
    
    Arrange: Make GET request to root
    Act: Follow redirects
    Assert: Final response has successful status code
    """
    # Arrange
    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert "/static/index.html" in response.headers["location"]
