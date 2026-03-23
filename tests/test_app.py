import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# AAA: Arrange-Act-Assert pattern

def test_get_activities():
    # Arrange
    # Nenhuma preparação extra necessária, pois o banco é em memória

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success():
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Cleanup: remove o usuário para não afetar outros testes
    client.post(f"/activities/{activity}/remove?email={email}")


def test_signup_duplicate():
    # Arrange
    email = "testuser2@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Cleanup
    client.post(f"/activities/{activity}/remove?email={email}")


def test_remove_participant_success():
    # Arrange
    email = "testuser3@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity}/remove?email={email}")

    # Assert
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" in response.json()["message"]


def test_remove_participant_not_found():
    # Arrange
    email = "notregistered@mergington.edu"
    activity = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity}/remove?email={email}")

    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_signup_activity_not_found():
    # Arrange
    email = "testuser4@mergington.edu"
    activity = "Nonexistent Activity"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
