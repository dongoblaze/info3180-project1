from flask import Flask
from flask_sqlalchemy import SQLAlchemy

UPLOAD_FOLDER = './app/static/uploads'
# Config Values

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://sohydtnhzkmbac:ba3db9d466e5aa0964683e57bb9c8020c8e1adc258a7a3301507185be987a756@ec2-18-235-97-230.compute-1.amazonaws.com:5432/deied3ba3oa5to"
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@localhost/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning
SECRET_KEY = 'Sup3r$3cretkey'
db = SQLAlchemy(app)


app.config.from_object(__name__)
from app import views