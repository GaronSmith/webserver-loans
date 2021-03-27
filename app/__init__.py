import os 
from flask import Flask, request, redirect
from flask_cors import CORS
from flask_migrate import migrate

app = Flask(__name__)
