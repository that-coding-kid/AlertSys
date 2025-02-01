from courier.client import Courier
import os
from dotenv import load_dotenv

load_dotenv()

def get_courier_client():
    auth_token = os.getenv("COURIER_API")
    if not auth_token:
        raise ValueError("COURIER_API token not found in environment variables")
    return Courier(authorization_token=auth_token)

def send_email_notification(email, name, severity, body):
    client = get_courier_client()
    resp = client.send(
        message={
            "to": {
                "email": email
            },
            "content": {
                "title": severity,
                "body": body
            },
            "data": {
                "name": name
            }
        }
    )
    return resp