"""Shared pytest fixtures for all tests"""

import pytest
import copy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Fixture providing a TestClient for API testing"""
    return TestClient(app)


@pytest.fixture
def fresh_activities():
    """Fixture providing a deep copy of activities for test isolation"""
    return copy.deepcopy(activities)


@pytest.fixture
def mock_activities(monkeypatch, fresh_activities):
    """
    Fixture that replaces the app's activities with fresh test data.
    Ensures each test gets isolated activities without state leakage.
    """
    monkeypatch.setattr("src.app.activities", fresh_activities)
    return fresh_activities
