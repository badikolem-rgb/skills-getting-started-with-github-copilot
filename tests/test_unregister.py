"""Tests for DELETE /activities/{activity_name}/participants/{email} endpoint"""

import pytest


def test_unregister_success_removes_participant(client, mock_activities):
    """
    Test successful unregister removes student from participants list
    
    Arrange: Get existing participant
    Act: Call DELETE to remove participant
    Assert: Student is removed from list
    """
    # Arrange
    activity_name = "Chess Club"
    email = mock_activities[activity_name]["participants"][0]
    initial_count = len(mock_activities[activity_name]["participants"])

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 200
    assert email not in mock_activities[activity_name]["participants"]
    assert len(mock_activities[activity_name]["participants"]) == initial_count - 1
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"


def test_unregister_activity_not_found(client, mock_activities):
    """
    Test unregister fails when activity doesn't exist
    
    Arrange: Use non-existent activity name
    Act: Call DELETE with invalid activity
    Assert: Returns 404 error
    """
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_student_not_registered(client, mock_activities):
    """
    Test unregister fails when student isn't registered
    
    Arrange: Use email not in participants list
    Act: Call DELETE for unregistered student
    Assert: Returns 400 error
    """
    # Arrange
    activity_name = "Chess Club"
    email = "notstudent@mergington.edu"
    initial_count = len(mock_activities[activity_name]["participants"])

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]
    assert len(mock_activities[activity_name]["participants"]) == initial_count


def test_unregister_response_format(client, mock_activities):
    """
    Test that unregister response has correct format
    
    Arrange: Valid unregister request
    Act: Call DELETE to remove participant
    Assert: Response contains message field
    """
    # Arrange
    activity_name = "Programming Class"
    email = mock_activities[activity_name]["participants"][0]

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert "message" in data
    assert isinstance(data["message"], str)
