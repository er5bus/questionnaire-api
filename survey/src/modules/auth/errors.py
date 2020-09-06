from ... import jwt
import sys, traceback
from werkzeug.exceptions import HTTPException, InternalServerError


@jwt.invalid_token_loader
def invalid_token_callback(error_string):
    return {"code": error_string.lower().replace(" ", "-"), "message": error_string }, 422


@jwt.unauthorized_loader
def unauthorized_callback(error_string):
    return {"code": "unauthorized", "message": error_string }, 401


@jwt.needs_fresh_token_loader
def needs_fresh_token_callback():
    return {"code": "unauthorized", "message": "Fresh token required" }, 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return {"code": "unauthorized", "message": "Token has been revoked" }, 401


@jwt.user_loader_error_loader
def user_loader_error_callback(identity):
    return {"code": "unauthorized", "message": "Error loading the user {}".format(identity) }, 401


@jwt.claims_verification_failed_loader
def verify_claims_failed_callback(identity):
    return {"code": "unauthorized", "message": "Error loading the user {}".format(identity) }, 401


@jwt.expired_token_loader
def expired_token_callback(expired_token):
    return {"code": "unauthorized", "message": "The {} token has expired".format(identity) }, 401
