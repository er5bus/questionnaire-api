from werkzeug.routing import IntegerConverter


class SignedIntConverter(IntegerConverter):
    regex = r'-?\d+'
