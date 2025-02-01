import pytest
from flask import json
from server import app
import importlib

from unittest.mock import patch, MagicMock
import os
from datetime import datetime

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_env_hash():
    """Mock environment variable for hash verification"""
    with patch.dict(os.environ, {'HASH': 'test_hash'}):
        yield

@pytest.fixture
def valid_user_data():
    return {
        "hash": "test_hash",
        "email": "test@example.com",
        "password": "test123",
        "name": "Test User",
        "mobile_number": "1234567890",
        "location": "Test City"
    }

@pytest.fixture
def valid_notification_data():
    return {
        "hash": "test_hash",
        "email": "test@example.com",
        "location": "Test City",
        "severity": "HIGH",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M:%S"),
        "text": "Test notification"
    }

class TestUserAPI:
    @pytest.mark.parametrize(
        "input_data,expected_status,expected_message",
        [
            ({"hash": "test_hash", "email": "test@example.com", "password": "test123"}, 200, "success"),
            ({"hash": "wrong_hash", "email": "test@example.com", "password": "test123"}, 200, "Invalid Hash"),
            ({"email": "test@example.com", "password": "test123"}, 200, "Invalid Hash"),
        ]
    )
    def test_user_login(self, client, mock_env_hash, input_data, expected_status, expected_message):
        with patch('server.get_user_details') as mock_get_user:
            mock_get_user.return_value = {"status": "success", "user": {"email": "test@example.com"}}
            response = client.get('/api/user', json=input_data)
            assert response.status_code == expected_status
            if expected_message == "success":
                assert json.loads(response.data)["status"] == "success"
            else:
                assert json.loads(response.data)["message"] == expected_message

    def test_user_registration(self, client, mock_env_hash, valid_user_data):
        with patch('server.register_user') as mock_register:
            mock_register.return_value = {"status": "success", "message": "User registered successfully"}
            response = client.post('/api/user', json=valid_user_data)
            assert response.status_code == 200
            assert json.loads(response.data)["status"] == "success"

class TestAdminAPI:
    def test_admin_login(self, client, mock_env_hash):
        admin_data = {
            "hash": "test_hash",
            "email": "admin@example.com",
            "password": "admin123"
        }
        with patch('server.get_admin_details') as mock_get_admin:
            mock_get_admin.return_value = {"status": "success", "user": {"email": "admin@example.com"}}
            response = client.get('/api/admin', json=admin_data)
            assert response.status_code == 200
            assert json.loads(response.data)["status"] == "success"

class TestNotificationAPI:
    def test_add_notification(self, client, mock_env_hash, valid_notification_data):
        with patch('server.add_notification') as mock_add_notification:
            mock_add_notification.return_value = {"status": "success", "message": "Notification added successfully"}
            response = client.post('/api/notification', json=valid_notification_data)
            assert response.status_code == 200
            assert json.loads(response.data)["status"] == "success"

    def test_get_notifications_by_admin(self, client, mock_env_hash):
        query_data = {
            "hash": "test_hash",
            "email": "admin@example.com"
        }
        with patch('server.fetch_notification_by_admin') as mock_fetch:
            mock_fetch.return_value = [{"notification": "test"}]
            response = client.get('/api/notification/admin', json=query_data)
            assert response.status_code == 200
            assert isinstance(json.loads(response.data), list)

    def test_get_notifications_by_location(self, client, mock_env_hash):
        query_data = {
            "hash": "test_hash",
            "location": "Test City"
        }
        with patch('server.fetch_notification_by_location') as mock_fetch:
            mock_fetch.return_value = [{"notification": "test"}]
            response = client.get('/api/notification/location', json=query_data)
            assert response.status_code == 200
            assert isinstance(json.loads(response.data), list)

class TestEmailAPI:
    def test_send_email(self, client, mock_env_hash):
        email_data = {
            "hash": "test_hash",
            "email": "test@example.com",
            "name": "Test User",
            "severity": "HIGH",
            "body": "Test notification body"
        }
        with patch('server.send_email_notification') as mock_send_email:
            mock_send_email.return_value = {"status": "success"}
            response = client.post('/api/send_email', json=email_data)
            assert response.status_code == 200

class TestDatabaseOperations:
    def test_user_registration_db(self, valid_user_data):
        # Mock setup
        mock_collection = MagicMock()
        mock_collection.find_one.return_value = None  # Simulate no existing user
        mock_db = MagicMock()
        mock_db.__getitem__.return_value = mock_collection  # mock_db["any_collection"] returns mock_collection

        # Patch AND reload module
        with patch('MongoDBConnector.get_database', return_value=mock_db):
            # Reload the module to re-initialize collections with the mock
            import NewUserRegistration
            importlib.reload(NewUserRegistration)
            from NewUserRegistration import register_user

            # Execute
            result = register_user(
                valid_user_data["email"],
                valid_user_data["password"],
                valid_user_data["name"],
                valid_user_data["mobile_number"],
                valid_user_data["location"]
            )

        # Assertions
        mock_collection.find_one.assert_called_once_with({"email": valid_user_data["email"]})
        mock_collection.insert_one.assert_called_once()

    def test_notification_db(self, valid_notification_data):
        # Mock setup
        mock_collection = MagicMock()
        mock_db = MagicMock()
        mock_db.__getitem__.return_value = mock_collection

        # Patch AND reload module
        with patch('MongoDBConnector.get_database', return_value=mock_db):
            # Reload the module to re-initialize collections with the mock
            import NotificationUtility
            importlib.reload(NotificationUtility)
            from NotificationUtility import add_notification

            # Execute
            result = add_notification(
                valid_notification_data["email"],
                valid_notification_data["location"],
                valid_notification_data["severity"],
                valid_notification_data["date"],
                valid_notification_data["time"],
                valid_notification_data["text"]
            )

        # Assertions
        mock_collection.insert_one.assert_called_once()