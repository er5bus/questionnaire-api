from . import api
import sys, traceback
from werkzeug.exceptions import HTTPException


@api.errorhandler(HTTPException)
def handle_exception(e):
    return {"error": e.name.lower().replace(" ", "-"), "message": e.description}, e.code

@api.errorhandler(Exception)
def handle_internal_exception(e):
    traceback.print_exc(file=sys.stdout)
    return {"error": "internal-error", "message": "something wrong happened"}, 500
