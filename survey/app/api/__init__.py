from flask import Blueprint


api = Blueprint('api', __name__)

from . import auth, company, account, employee, manager_invitation, medical_record, errors
