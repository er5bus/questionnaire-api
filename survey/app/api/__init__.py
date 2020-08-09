from flask import Blueprint


api = Blueprint('api', __name__)

from . import auth, company, account, employee, department, manager_invitation, employee_invitation, medical_record, errors
