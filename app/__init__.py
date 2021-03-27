import os 
from flask import Flask, request, redirect
from flask_cors import CORS
from flask_migrate import Migrate

from .config import Config
from .models import db

app = Flask(__name__)

app.config.from_object(Config)
db.init_app(app)

CORS(app)

