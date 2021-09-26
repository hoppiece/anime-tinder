import os
from typing import Dict
from os.path import join, dirname
from dotenv import load_dotenv

envdir = join(dirname(__file__), "../../env/")

if os.path.exists(join(envdir, ".env.prod")):
    dotenv_path = join(envdir, ".env.prod")
    IS_LOCAL = False
elif os.path.exists(join(dirname(__file__), "../.env.prod")):
    dotenv_path = join(dirname(__file__), "../.env.prod")
    IS_LOCAL = True
else:
    print("env file does not exist.")
    exit()

load_dotenv(dotenv_path)

ENV_VALUES: Dict[str, str] = {
    "CONSUMER_API_KEY": os.environ.get("CONSUMER_API_KEY", ""),
    "CONSUMER_SECRET_KEY": os.environ.get("CONSUMER_SECRET_KEY", ""),
    "APP_URL": os.environ.get("APP_URL", ""),
    "SERVER_URL": os.environ.get("SERVER_URL", ""),
    "DB_USER": os.environ.get("DB_USER", ""),
    "DB_PW": os.environ.get("DB_PW", ""),
    "DB_HOST": os.environ.get("DB_HOST", ""),
    "DB_NAME": os.environ.get("DB_NAME", ""),
}
