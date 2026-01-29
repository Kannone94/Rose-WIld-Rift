from requests import session
import os
from dotenv import load_dotenv

load_dotenv()

def login(username, password):
    login_url = os.getenv("login_url")
    session = session()
    response = session.post(login_url, data={"username": username, "password": password})
    return response.status_code == 200  # Return True if login was successful