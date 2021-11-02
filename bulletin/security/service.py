import jwt
from django.conf import settings

from .dto.login_info import LoginInfo
from member.service import MemberService


class LoginService:
    def __init__(self):
        self.member_service = MemberService()

    def authenticate(self, info: LoginInfo):
        member = self.member_service.get_member(username=info.username)
        if member is None:
            # todo: create MemberNotFoundException
            raise Exception

        if member.password == info.password:
            return jwt.encode(
                payload={
                    "username": info.username
                },
                key=settings.JWT_SECRET,
                algorithm=settings.JWT_ALGORITHM
            )
        else:
            # todo: create IncorrectPasswordException
            raise Exception
