from flask import Blueprint


api = Blueprint('manager', __name__)

from . import urls
