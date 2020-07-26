from .. import db
from ._behaviors import Base
from .common import BaseInvitation, BaseUser
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData


class Manager(BaseUser):

    __mapper_args__ = {'polymorphic_identity':'manager'}

    #phone = db.Column(db.String(20))



class ManagerInvitation(BaseInvitation):

    __mapper_args__ = {'polymorphic_identity':'managerinvitation'}

    def generate_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({ 'pk': str(self.pk), 'company_pk': self.company_pk, 'invitation': self.__class__.__name__ }).decode('utf-8')
