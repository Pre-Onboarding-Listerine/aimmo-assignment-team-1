from functools import wraps

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
            return "Bearer " + jwt.encode(
                payload={
                    "username": info.username
                },
                key=settings.JWT_SECRET,
                algorithm=settings.JWT_ALGORITHM
            )
        else:
            # todo: create IncorrectPasswordException
            raise Exception


def authorize(method):
    member_service = MemberService()

    @wraps(method)
    def wrapper(self, request, *args, **kwargs):
        access_token = request.headers.get("Authorization")
        if access_token is None:
            # todo: AuthorizationHeaderEmptyException
            raise Exception
        access_token = access_token[len("Bearer "):]
        try:
            payload = jwt.decode(access_token, settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHM)
            member = member_service.get_member(payload.get("username"))
            return method(self, request, member, *args, **kwargs)
        except jwt.InvalidSignatureError:
            # todo: UnauthorizedException
            raise Exception
    return wrapper
