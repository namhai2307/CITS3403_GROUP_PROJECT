from flask import Flask

app = Flask(__name__)

#if you want to test the file locally, need to add your own secret key here [temporary solution]
app.config["SECRET_KEY"] = 'secretkey'

from app import routes, forms
