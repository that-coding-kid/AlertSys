from flask import Flask, jsonify, request
import os
from bson import json_util
import json

from AdminDetailFetch import get_admin_details 
from UserDetailFetch import get_user_details
from NewUserRegistration import register_user
from NotificationUtility import fetch_notification_by_admin, fetch_notification_by_location 
from SendEmailNotification import send_email_notification

app = Flask(__name__)

@app.route('/api/user', methods=['GET'])
def user_login():
    data = request.json
    try:
        hash = data.get('hash')
    except:
        return jsonify({'message': 'Invalid Hash'})
    hash = data.get('hash')
    if hash == os.getenv('HASH'):
        email = data.get('email')
        password = data.get('password')
        result = get_user_details(email, password)
        return json.loads(json_util.dumps(result))
    else:
        return jsonify({'message': 'Invalid Hash'})
@app.route('/api/user', methods=['POST'])
def create_user():
    data = request.json
    try:
        hash = data.get('hash')
    except:
        return jsonify({'message': 'Invalid Hash'})
    hash = data.get('hash')
    if hash == os.getenv('HASH'):
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        mobile_number = data.get('mobile_number')
        location = data.get('location')
        result = register_user(email, password, name, mobile_number, location)
        return json.loads(json_util.dumps(result))

@app.route('/api/admin', methods=['GET'])
def admin_login():
    data = request.json
    try:
        hash = data.get('hash')
    except:
        return jsonify({'message': 'Invalid Hash'})
    hash = data.get('hash')
    if hash == os.getenv('HASH'):
        email = data.get('email')
        password = data.get('password')
        result = get_admin_details(email, password)
        return json.loads(json_util.dumps(result))

@app.route('/api/notification/admin', methods=['GET'])
def get_notifications_by_admin():
    data = request.json
    try:
        hash = data.get('hash')
    except:
        return jsonify({'message': 'Invalid Hash'})
    hash = data.get('hash')
    email = data.get('email')
    if hash == os.getenv('HASH'):
        result = fetch_notification_by_admin(email)
        return json.loads(json_util.dumps(result))

@app.route('/api/notification/location', methods=['GET'])
def get_notifications_by_location():
    data = request.json
    try:
        hash = data.get('hash')
    except:
        return jsonify({'message': 'Invalid Hash'})
    hash = data.get('hash')
    location = data.get('location')
    if hash == os.getenv('HASH'):
        result = fetch_notification_by_location(location)
        return json.loads(json_util.dumps(result))

@app.route('/api/notification', methods=['POST'])
def add_notification():
    data = request.json
    try:
        hash = data.get('hash')
    except:
        return jsonify({'message': 'Invalid Hash'})
    hash = data.get('hash')
    if hash == os.getenv('HASH'):
        email = data.get('email')
        location = data.get('location')
        severity = data.get('severity')
        date = data.get('date')
        time = data.get('time')
        text = data.get('text')
        result = add_notification(email, location, severity, date, time, text)
        return json.loads(json_util.dumps(result))

@app.route('/api/send_email', methods=['POST'])
def send_email():
    data = request.json
    try:
        hash = data.get('hash')
    except:
        return jsonify({'message': 'Invalid Hash'})
    hash = data.get('hash')
    if hash == os.getenv('HASH'):
        email = data.get('email')
        name = data.get('name')
        severity = data.get('severity')
        body = data.get('body')
        result = send_email_notification(email, name, severity, body)
        return json.loads(json_util.dumps(result))

if __name__ == '__main__':
    app.run(debug=True)
    print("hello")