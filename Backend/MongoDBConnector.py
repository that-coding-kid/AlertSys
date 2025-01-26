from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()

def get_database():
   CONNECTION_STRING = os.getenv("MONGODB_URL")
   client = MongoClient(CONNECTION_STRING)
   return client['DisasterAlertSystem']
  
if __name__ == "__main__":   
   dbname = get_database()