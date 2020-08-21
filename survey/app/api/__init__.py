from flask import Blueprint


api = Blueprint('api', __name__)

from . import auth, company, account, employee, manager, department, manager_invitation, employee_invitation, medical_record, accept_invitation, question_history, errors
