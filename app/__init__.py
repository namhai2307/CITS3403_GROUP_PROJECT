from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin
from config import Config
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['DEBUG'] = True  # Enable debug mode

db = SQLAlchemy(app)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(28), nullable=False)
    password = db.Column(db.String(88), nullable=False)

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired()])

"""@app.route("/")  
def home():
    return render_template("index.html")"""

@app.route('/')
def login():
    return render_template('sign_up_page.html')


#if __name__ == "__main__":
#    app.run(debug=True)