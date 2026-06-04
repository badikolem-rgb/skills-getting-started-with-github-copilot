"""Tests for GET /activities endpoint"""

import pytest


def test_get_activities_returns_all_activities(client, mock_activities):
    """
    Test that GET /activities returns all activities
    
    Arrange: Set up fresh activities
    Act: Call GET /activities
    Assert: Response includes all activities
    """
    # Arrange
    expected_activity_count = len(mock_activities)

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert len(data) == expected_activity_count


def test_get_activities_has_correct_structure(client, mock_activities):
    """
    Test that each activity has required fields
    
    Arrange: Expected activity fields
    Act: Call GET /activities
    Assert: Verify each activity has description, schedule, max_participants, participants
    """
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    assert response.status_code == 200
    for activity_name, activity_data in activities.items():
        assert set(activity_data.keys()) == required_fields


def test_get_activities_participants_is_list(client, mock_activities):
    """
    Test that participants field is always a list
    
    Arrange: Get activities
    Act: Call GET /activities
    Assert: All participants fields are lists
    """
    # Arrange
    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    assert response.status_code == 200
    for activity_data in activities.values():
        assert isinstance(activity_data["participants"], list)


def test_get_activities_max_participants_is_positive(client, mock_activities):
    """
    Test that max_participants values are positive integers
    
    Arrange: Call GET /activities
    Act: Fetch all activities
    Assert: max_participants is a positive integer for each activity
    """
    # Arrange
    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    assert response.status_code == 200
    for activity_data in activities.values():
        assert isinstance(activity_data["max_participants"], int)
        assert activity_data["max_participants"] > 0
