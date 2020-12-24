from dotenv import load_dotenv
from os import environ

load_dotenv()

class Config:

    def __init__(self):
        self.APP_KEY_ID = environ["APP_KEY_ID"]
        self.APP_KEY = environ["APP_KEY"]

config = Config()