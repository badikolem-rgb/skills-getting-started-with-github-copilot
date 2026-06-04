"""End-to-end integration tests"""

import pytest


def test_signup_then_appears_in_activities_list(client, mock_activities):
    """
    Test end-to-end: signup adds participant to activities list
    
    Arrange: Prepare new student email
    Act: 1) Sign up, 2) Fetch activities
    Assert: New participant appears in activities list
    """
    # Arrange
    activity_name = "Programming Class"
    email = "newdev@mergington.edu"

    # Act - Sign up
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    # Act - Fetch activities
    activities_response = client.get("/activities")

    # Assert
    assert activities_response.status_code == 200
    activity_data = activities_response.json()[activity_name]
    assert email in activity_data["participants"]


def test_signup_unregister_flow(client, mock_activities):
    """
    Test complete flow: signup → unregister
    
    Arrange: New student email
    Act: 1) Sign up, 2) Unregister, 3) Verify removal
    Assert: Student appears then disappears
    """
    # Arrange
    activity_name = "Gym Class"
    email = "athlete@mergington.edu"

    # Act - Sign up
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200
    assert email in mock_activities[activity_name]["participants"]

    # Act - Unregister
    unregister_response = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert unregister_response.status_code == 200

    # Assert
    assert email not in mock_activities[activity_name]["participants"]


def test_multiple_signups_same_activity(client, mock_activities):
    """
    Test multiple different students can sign up for same activity
    
    Arrange: Multiple student emails
    Act: Each student signs up for same activity
    Assert: All students in participants list
    """
    # Arrange
    activity_name = "Drama Club"
    students = [
        "actor1@mergington.edu",
        "actor2@mergington.edu",
        "actor3@mergington.edu"
    ]

    # Act
    for email in students:
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == 200

    # Assert
    participants = mock_activities[activity_name]["participants"]
    for email in students:
        assert email in participants


def test_signup_across_multiple_activities(client, mock_activities):
    """
    Test one student can sign up for multiple different activities
    
    Arrange: One student email, multiple activities
    Act: Student signs up for each activity
    Assert: Student appears in all activities
    """
    # Arrange
    email = "busy@mergington.edu"
    activities_to_join = ["Science Olympiad", "Debate Team", "Art Studio"]

    # Act
    for activity_name in activities_to_join:
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == 200

    # Assert
    for activity_name in activities_to_join:
        assert email in mock_activities[activity_name]["participants"]


def test_signup_then_unregister_multiple_students(client, mock_activities):
    """
    Test signup and unregister with multiple students
    
    Arrange: Multiple student emails
    Act: 1) All sign up, 2) Some unregister, 3) Verify state
    Assert: Correct students remain and removed ones are gone
    """
    # Arrange
    activity_name = "Soccer Team"
    students_to_add = ["player1@mergington.edu", "player2@mergington.edu", "player3@mergington.edu"]
    students_to_remove = ["player1@mergington.edu", "player3@mergington.edu"]

    # Act - All sign up
    for email in students_to_add:
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == 200

    # Act - Some unregister
    for email in students_to_remove:
        response = client.delete(f"/activities/{activity_name}/participants/{email}")
        assert response.status_code == 200

    # Assert - Verify final state
    participants = mock_activities[activity_name]["participants"]
    assert "player1@mergington.edu" not in participants
    assert "player2@mergington.edu" in participants
    assert "player3@mergington.edu" not in participants


def test_activity_count_updates_after_operations(client, mock_activities):
    """
    Test that participant count reflects signup/unregister operations
    
    Arrange: Get initial participant count
    Act: 1) Sign up 2 students, 2) Unregister 1, 3) Get updated count
    Assert: Count changes correctly
    """
    # Arrange
    activity_name = "Basketball Club"
    initial_count = len(mock_activities[activity_name]["participants"])
    students = ["baller1@mergington.edu", "baller2@mergington.edu"]

    # Act - Add 2 students
    for email in students:
        client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act - Remove 1 student
    client.delete(f"/activities/{activity_name}/participants/{students[0]}")

    # Assert - Count should be initial + 1
    response = client.get("/activities")
    final_count = len(response.json()[activity_name]["participants"])
    assert final_count == initial_count + 1
