from courier.client import Courier
import os
from dotenv import load_dotenv

load_dotenv()

client = Courier(
  authorization_token=os.getenv("COURIER_API")
)

def send_email_notification(email, name, body):
  resp = client.send(
    message={
      "to": {
        "email": email
      },
      "content": {
        "title": 'Disaster Alert!',
        "body": body
      },
      "data": {
        "name": name
      }
    }
  )

  return(resp)

