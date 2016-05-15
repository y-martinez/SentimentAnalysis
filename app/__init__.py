from flask import Flask
from config import *

app = Flask(__name__, template_folder='templates', static_folder='statics')
app.config.from_object('config')

from app import controller