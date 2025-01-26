from MongoDBConnector import get_database
dbname = get_database()
collection_name = dbname["notification_data"]

def add_notification(email, location, date, time, text):
    new_notification = {
        "email": email,
        "location": location,
        "date": date,
        "time": time,
        "text": text
    }
    collection_name.insert_one(new_notification)
    return {"status": "success", "message": "Notification added successfully"}

def fetch_notification_by_admin(email):
    return list(collection_name.find({"email": email}))

def fetch_notification_by_location(location):
    return list(collection_name.find({"location": location}))