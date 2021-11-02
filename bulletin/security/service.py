from functools import wraps
from http import HTTPStatus

import jwt
from django.conf import settings
from django.http import JsonResponse

from .dto.login_info import LoginInfo
from member.service import MemberService

from member.exceptions import MemberNotFoundException

from .exceptions import IncorrectPasswordException


class LoginService:
    def __init__(self):
        self.member_service = MemberService()

    def authenticate(self, info: LoginInfo):
        member = self.member_service.get_member(username=info.username)
        if member is None:
            raise MemberNotFoundException

        if member.password == info.password:
            return "Bearer " + jwt.encode(
                payload={
                    "username": info.username
                },
                key=settings.JWT_SECRET,
                algorithm=settings.JWT_ALGORITHM
            )
        else:
            raise IncorrectPasswordException


def authorize(method):
    member_service = MemberService()

    @wraps(method)
    def wrapper(self, request, *args, **kwargs):
        access_token = request.headers.get("Authorization")
        if access_token is None:
            return JsonResponse(data={}, status=HTTPStatus.UNAUTHORIZED)
        access_token = access_token[len("Bearer "):]
        try:
            payload = jwt.decode(access_token, settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHM)
            member = member_service.get_member(payload.get("username"))
            return method(self, request, member, *args, **kwargs)
        except jwt.InvalidSignatureError:
            return JsonResponse(data={}, status=HTTPStatus.UNAUTHORIZED)
    return wrapper


def general_authorize(method):
    member_service = MemberService()

    @wraps(method)
    def wrapper(self, request, *args, **kwargs):
        access_token = request.headers.get("Authorization")
        if access_token is None:
            return method(self, request, None, *args, **kwargs)
        access_token = access_token[len("Bearer "):]
        try:
            payload = jwt.decode(access_token, settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHM)
            member = member_service.get_member(payload.get("username"))
            return method(self, request, member, *args, **kwargs)
        except jwt.InvalidSignatureError:
            return JsonResponse(data={}, status=HTTPStatus.UNAUTHORIZED)
    return wrapper
