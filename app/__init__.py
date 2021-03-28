import os 
from flask import Flask, request, redirect
from flask_cors import CORS
from flask_migrate import Migrate

from .config import Config
from .models import db
from .api.loan_routes import loan_routes

app = Flask(__name__)

app.config.from_object(Config)
app.register_blueprint(loan_routes, url_prefix="/api/loans")
db.init_app(app)
Migrate(app,db)

CORS(app)

@app.before_request
def https_redirect():
    if os.environ.get('FLASK_ENV') == 'production':
        if request.headers.get('X-Forwarded-Proto') == 'http':
            url = request.url.replace('http://', 'https://', 1)
            code = 301
            return redirect(url, code=code)



