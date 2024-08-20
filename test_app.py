import pytest
from app import app, random_fruit


@pytest.fixture
def client():
    """Fixture providing a Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_random_fruit():
    """Test the random_fruit function"""
    fruits = ["apple", "cherry", "orange"]
    result = random_fruit()
    assert result[0] in fruits


def test_fruit_route(client):
    """Test the "/" route for correct response and template rendering"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Random Fruit" in response.data

    # Ensure the random fruit is rendered in the template
    fruits = [b"apple", b"cherry", b"orange"]
    found_fruit = any(fruit in response.data for fruit in fruits)
    assert found_fruit, "The template does not contain a valid fruit."


@pytest.mark.parametrize("fruit", ["apple", "cherry", "orange"])
def test_fruit_in_template(client, monkeypatch, fruit):
    """Test that the random fruit is correctly displayed in the template."""

    # Use monkeypatch to mock random_fruit to always return the specified fruit
    monkeypatch.setattr("app.random_fruit", lambda: [fruit])

    response = client.get("/")
    assert response.status_code == 200
    assert bytes(fruit, "utf-8") in response.data
