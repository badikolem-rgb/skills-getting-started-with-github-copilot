"""Tests for POST /activities/{activity_name}/signup endpoint"""

import pytest


def test_signup_success_adds_participant(client, mock_activities):
    """
    Test successful signup adds student to participants list
    
    Arrange: Prepare email and activity name
    Act: Call POST /activities/Chess Club/signup
    Assert: Student email is in participants list
    """
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    initial_count = len(mock_activities[activity_name]["participants"])

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert email in mock_activities[activity_name]["participants"]
    assert len(mock_activities[activity_name]["participants"]) == initial_count + 1
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"


def test_signup_activity_not_found(client, mock_activities):
    """
    Test signup fails when activity doesn't exist
    
    Arrange: Use non-existent activity name
    Act: Call POST with invalid activity
    Assert: Returns 404 error
    """
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_student_rejected(client, mock_activities):
    """
    Test that duplicate signup is rejected
    
    Arrange: Get existing participant email
    Act: Try to sign up same student again
    Assert: Returns 400 error
    """
    # Arrange
    activity_name = "Chess Club"
    email = mock_activities[activity_name]["participants"][0]
    initial_count = len(mock_activities[activity_name]["participants"])

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    assert len(mock_activities[activity_name]["participants"]) == initial_count


@pytest.mark.parametrize("activity_name", [
    "Chess Club",
    "Programming Class",
    "Gym Class",
    "Soccer Team",
    "Basketball Club"
])
def test_signup_works_for_all_activities(client, mock_activities, activity_name):
    """
    Test signup works for multiple different activities
    
    Arrange: Parameterized activity names
    Act: Sign up for each activity
    Assert: All signups successful
    """
    # Arrange
    email = "testuser@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert email in mock_activities[activity_name]["participants"]


def test_signup_response_format(client, mock_activities):
    """
    Test that signup response has correct format
    
    Arrange: Valid signup request
    Act: Call POST /activities/{activity}/signup
    Assert: Response contains message field
    """
    # Arrange
    activity_name = "Art Studio"
    email = "artist@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert "message" in data
    assert isinstance(data["message"], str)
