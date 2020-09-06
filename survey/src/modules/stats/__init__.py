from flask import Blueprint


api = Blueprint('stats', __name__)

from . import urls
