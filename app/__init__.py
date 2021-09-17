import os
import json

from pathlib import Path

import psycopg2

from flask import Flask
from flask_restx import Api


base_dir = Path(__file__).resolve().parent.parent
config_dir = os.path.join(base_dir, "config")
config_file = os.path.join(config_dir, "config.json")
config = json.loads(open(config_file).read())

db = psycopg2.connect(
    dbname=config["db"]["database"],
    user=config["db"]["username"],
    password=config["db"]["password"],
    host=config["db"]["host"],
    port=config["db"]["port"],
)

app = Flask(__name__)
api = Api(app, version="1.0", title="Healthcare API", description="A simple API")


from app.person import Person
from app.visit import Visit


api.add_namespace(Person, "/person")
api.add_namespace(Visit, "/visit")
