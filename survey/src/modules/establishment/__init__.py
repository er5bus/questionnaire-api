from flask import Blueprint


api = Blueprint('establishment', __name__)

from . import urls
