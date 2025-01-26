from MongoDBConnector import get_database
dbname = get_database()
collection_name = dbname["user_data"]

def register_user(email, password, name, mobile_number, location, date_of_birth, gender):
    if collection_name.find_one({"email": email}):
        return {"status": "error", "message": "User already exists"}

    new_user = {
        "email": email,
        "password": password,
        "name": name,
        "mobile_number": mobile_number,
        "location": location,
        "date_of_birth": date_of_birth,
        "gender": gender
    }
    collection_name.insert_one(new_user)
    return {"status": "success", "message": "User registered successfully"}


