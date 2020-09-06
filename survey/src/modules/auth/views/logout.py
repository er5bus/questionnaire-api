from .... import jwt
from ....tools.views import generics
from flask_jwt_extended import get_jwt_identity, get_raw_jwt, get_jti, jwt_required


blacklist = set()
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token["jti"]
    return jti in blacklist

class BaseUserLogoutView(generics.CreateAPIView):

    route_path = "/auth/logout"
    route_name = "user_logout"

    decorators = [jwt_required]

    def post(self, *args, **kwargs):
        jti = get_raw_jwt()["jti"]
        blacklist.add(jti)
        return {"message": "Successfully logged out"}, 200
