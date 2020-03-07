from flask import Flask
UPLOAD_FOLDER = './app/static/uploads'
# Config Values

SECRET_KEY = 'Sup3r$3cretkey'



app = Flask(__name__)
app.config.from_object(__name__)
from app import views