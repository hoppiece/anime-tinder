import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

ENV_VALUES = {
    "CONSUMER_API_KEY": os.environ.get("CONSUMER_API_KEY"),
    "CONSUMER_SECRET_KEY": os.environ.get("CONSUMER_SECRET_KEY"),
    "APP_URL": os.environ.get("APP_URL"),
    "SERVER_URL": os.environ.get("SERVER_URL"),
}
