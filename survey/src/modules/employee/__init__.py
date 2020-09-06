from flask import Blueprint


api = Blueprint('employee', __name__)

from . import urls
