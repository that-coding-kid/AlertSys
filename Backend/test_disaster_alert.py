import pytest
from flask import json
from server import app
import importlib
from unittest.mock import patch, MagicMock
import os
from datetime import datetime
import csv
import json

# Load test cases from JSON file
def load_test_cases():
    with open("test_cases.json", "r") as file:
        return json.load(file)

# Fixtures
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

# CSV Logging Setup
def log_test_result(test_case_id, description, input_data, expected_output, actual_output, status):
    with open("test_log.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([test_case_id, description, input_data, expected_output, actual_output, status])

# Load test cases
test_cases = load_test_cases()

# Test Classes
class TestUserAPI:
    @pytest.mark.parametrize(
        "test_case",
        test_cases["user_login"],
        ids=[tc["test_case_id"] for tc in test_cases["user_login"]]
    )
    def test_user_login(self, client, mock_env_hash, test_case):
        with patch('server.get_user_details') as mock_get_user:
            mock_get_user.return_value = {"status": "success", "user": {"email": "test@example.com"}}
            response = client.get('/api/user', json=test_case["input"])
            data = json.loads(response.data)

            # Log the test result
            log_test_result(
                test_case_id=test_case["test_case_id"],
                description=test_case["description"],
                input_data=test_case["input"],
                expected_output={"status": test_case["expected_status"], "message": test_case["expected_message"]},
                actual_output=data,
                status="PASS" if data.get("status") == test_case["expected_status"] else "FAIL"
            )

            assert response.status_code == 200
            if test_case["expected_message"] == "success":
                assert data["status"] == "success"
            else:
                assert test_case["expected_message"] in data.get("message", "")

    @pytest.mark.parametrize(
        "test_case",
        test_cases["user_registration"],
        ids=[tc["test_case_id"] for tc in test_cases["user_registration"]]
    )
    def test_user_registration(self, client, mock_env_hash, test_case):
        with patch('server.register_user') as mock_register:
            mock_register.return_value = {"status": "success", "message": "User registered successfully"}
            response = client.post('/api/user', json=test_case["input"])
            data = json.loads(response.data)

            # Log the test result
            log_test_result(
                test_case_id=test_case["test_case_id"],
                description=test_case["description"],
                input_data=test_case["input"],
                expected_output={"status": test_case["expected_status"], "message": test_case["expected_message"]},
                actual_output=data,
                status="PASS" if data.get("status") == "success" else "FAIL"
            )

            assert response.status_code == 200
            assert data["status"] == "success"

class TestAdminAPI:
    @pytest.mark.parametrize(
        "test_case",
        test_cases["admin_login"],
        ids=[tc["test_case_id"] for tc in test_cases["admin_login"]]
    )
    def test_admin_login(self, client, mock_env_hash, test_case):
        with patch('server.get_admin_details') as mock_get_admin:
            mock_get_admin.return_value = {"status": "success", "user": {"email": "admin@example.com"}}
            response = client.get('/api/admin', json=test_case["input"])
            data = json.loads(response.data)

            # Log the test result
            log_test_result(
                test_case_id=test_case["test_case_id"],
                description=test_case["description"],
                input_data=test_case["input"],
                expected_output={"status": test_case["expected_status"], "user": {"email": "admin@example.com"}},
                actual_output=data,
                status="PASS" if data.get("status") == "success" else "FAIL"
            )

            assert response.status_code == 200
            assert data["status"] == "success"

class TestNotificationAPI:
    @pytest.mark.parametrize(
        "test_case",
        test_cases["add_notification"],
        ids=[tc["test_case_id"] for tc in test_cases["add_notification"]]
    )
    def test_add_notification(self, client, mock_env_hash, test_case):
        with patch('server.add_notification') as mock_add_notification:
            mock_add_notification.return_value = {"status": "success", "message": "Notification added successfully"}
            response = client.post('/api/notification', json=test_case["input"])
            data = json.loads(response.data)

            # Log the test result
            log_test_result(
                test_case_id=test_case["test_case_id"],
                description=test_case["description"],
                input_data=test_case["input"],
                expected_output={"status": test_case["expected_status"], "message": test_case["expected_message"]},
                actual_output=data,
                status="PASS" if data.get("status") == "success" else "FAIL"
            )

            assert response.status_code == 200
            assert data["status"] == "success"

    @pytest.mark.parametrize(
        "test_case",
        test_cases["get_notifications_by_admin"],
        ids=[tc["test_case_id"] for tc in test_cases["get_notifications_by_admin"]]
    )
    def test_get_notifications_by_admin(self, client, mock_env_hash, test_case):
        with patch('server.fetch_notification_by_admin') as mock_fetch:
            mock_fetch.return_value = [{"notification": "test"}]
            response = client.get('/api/notification/admin', json=test_case["input"])
            data = json.loads(response.data)

            # Log the test result
            log_test_result(
                test_case_id=test_case["test_case_id"],
                description=test_case["description"],
                input_data=test_case["input"],
                expected_output=test_case["expected_output"],
                actual_output=data,
                status="PASS" if isinstance(data, list) else "FAIL"
            )

            assert response.status_code == 200
            assert isinstance(data, list)

    @pytest.mark.parametrize(
        "test_case",
        test_cases["get_notifications_by_location"],
        ids=[tc["test_case_id"] for tc in test_cases["get_notifications_by_location"]]
    )
    def test_get_notifications_by_location(self, client, mock_env_hash, test_case):
        with patch('server.fetch_notification_by_location') as mock_fetch:
            mock_fetch.return_value = [{"notification": "test"}]
            response = client.get('/api/notification/location', json=test_case["input"])
            data = json.loads(response.data)

            # Log the test result
            log_test_result(
                test_case_id=test_case["test_case_id"],
                description=test_case["description"],
                input_data=test_case["input"],
                expected_output=test_case["expected_output"],
                actual_output=data,
                status="PASS" if isinstance(data, list) else "FAIL"
            )

            assert response.status_code == 200
            assert isinstance(data, list)

class TestEmailAPI:
    @pytest.mark.parametrize(
        "test_case",
        test_cases["send_email"],
        ids=[tc["test_case_id"] for tc in test_cases["send_email"]]
    )
    def test_send_email(self, client, mock_env_hash, test_case):
        with patch('server.send_email_notification') as mock_send_email:
            mock_send_email.return_value = {"status": "success"}
            response = client.post('/api/send_email', json=test_case["input"])
            data = json.loads(response.data)

            # Log the test result
            log_test_result(
                test_case_id=test_case["test_case_id"],
                description=test_case["description"],
                input_data=test_case["input"],
                expected_output={"status": test_case["expected_status"]},
                actual_output=data,
                status="PASS" if data.get("status") == "success" else "FAIL"
            )

            assert response.status_code == 200

class TestDatabaseOperations:
    @pytest.mark.parametrize(
        "test_case",
        test_cases["database_operations"],
        ids=[tc["test_case_id"] for tc in test_cases["database_operations"]]
    )
    def test_user_registration_db(self, client, mock_env_hash, test_case):
        # Mock setup
        mock_collection = MagicMock()
        mock_collection.find_one.return_value = None  # Simulate no existing user
        mock_db = MagicMock()
        mock_db.__getitem__.return_value = mock_collection

        # Patch AND reload module
        with patch('MongoDBConnector.get_database', return_value=mock_db):
            import NewUserRegistration
            importlib.reload(NewUserRegistration)
            from NewUserRegistration import register_user

            # Execute
            result = register_user(
                test_case["input"]["email"],
                test_case["input"]["password"],
                test_case["input"]["name"],
                test_case["input"]["mobile_number"],
                test_case["input"]["location"]
            )

            # Log the test result
            log_test_result(
                test_case_id=test_case["test_case_id"],
                description=test_case["description"],
                input_data=test_case["input"],
                expected_output={"status": test_case["expected_status"], "message": test_case["expected_message"]},
                actual_output=result,
                status="PASS" if result.get("status") == "success" else "FAIL"
            )

            # Assertions
            mock_collection.find_one.assert_called_once_with({"email": test_case["input"]["email"]})
            mock_collection.insert_one.assert_called_once()

    @pytest.mark.parametrize(
        "test_case",
        test_cases["database_operations"],
        ids=[tc["test_case_id"] for tc in test_cases["database_operations"]]
    )
    def test_notification_db(self, client, mock_env_hash, test_case):
        # Mock setup
        mock_collection = MagicMock()
        mock_db = MagicMock()
        mock_db.__getitem__.return_value = mock_collection

        # Patch AND reload module
        with patch('MongoDBConnector.get_database', return_value=mock_db):
            import NotificationUtility
            importlib.reload(NotificationUtility)
            from NotificationUtility import add_notification

            # Execute
            result = add_notification(
                test_case["input"]["email"],
                test_case["input"]["location"],
                test_case["input"]["severity"],
                test_case["input"]["date"],
                test_case["input"]["time"],
                test_case["input"]["text"]
            )

            # Log the test result
            log_test_result(
                test_case_id=test_case["test_case_id"],
                description=test_case["description"],
                input_data=test_case["input"],
                expected_output={"status": test_case["expected_status"], "message": test_case["expected_message"]},
                actual_output=result,
                status="PASS" if result.get("status") == "success" else "FAIL"
            )

            # Assertions
            mock_collection.insert_one.assert_called_once()