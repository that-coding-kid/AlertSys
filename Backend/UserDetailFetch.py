from MongoDBConnector import get_database
dbname = get_database()
collection_name = dbname["user_data"]

def get_user_details(email, password):
    user = collection_name.find_one({"email": email, "password": password})
    if user:
        return {"status": "success", "user": user}
    else:
        return {"status": "error", "message": "Invalid email or password"}