import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

# Copy the original activities for resetting
original_activities = activities.copy()

@pytest.fixture(autouse=True)
def reset_activities():
    activities.clear()
    activities.update(original_activities)

client = TestClient(app)

def test_get_activities():
    # Arrange - activities are reset
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert response.json() == activities

def test_signup_success():
    # Arrange
    activity_name = "Chess Club"
    email = "new@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities[activity_name]["participants"]

def test_signup_activity_not_found():
    # Arrange
    activity_name = "Nonexistent"
    email = "test@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}

def test_signup_already_signed_up():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # already in participants
    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}

def test_unregister_success():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in activities[activity_name]["participants"]

def test_unregister_activity_not_found():
    # Arrange
    activity_name = "Nonexistent"
    email = "test@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})
    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}

def test_unregister_not_signed_up():
    # Arrange
    activity_name = "Chess Club"
    email = "notsigned@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})
    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student not signed up for this activity"}