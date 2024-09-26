import os 
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List

load_dotenv()

EMAIL_HOST=os.environ.get("EMAIL_HOST")
EMAIL_HOST_PASSWORD=os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER=os.environ.get("EMAIL_ROST_USER")
EMAIL_PORT=os.environ.get("EMAIL_PORT")
EMAIL_BACKEND=os.environ.get("EMAIL_BACKEND")
USER_DB=os.environ.get("USER_DB")
PASSWORD_DB=os.environ.get("PASSWORD_DB")
HOST_DB=os.environ.get("HOST_DB")
NAME_DB=os.environ.get("NAME_DB")
PORT_DB=os.environ.get("PORT_DB")
SECRET_KEY=os.environ.get("SECRET_KEY")
GEMINI_API_KEY=os.environ.get("GEMINI_API_KEY")

