import os 
from flask import Flask, request, redirect
from flask_cors import CORS
from flask_migrate import migrate

from .config import Config

app = Flask(__name__)

app.config.from_object(Config)

CORS(app)

