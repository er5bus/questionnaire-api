from flask import Blueprint


api = Blueprint('questionnaire', __name__)

from . import urls
