import json
from http import HTTPStatus

from django.http import JsonResponse, HttpRequest
from django.views import View

from .dto.login_info import LoginInfo
from .exceptions import IncorrectPasswordException
from .service import LoginService
from member.exceptions import MemberNotFoundException


class LoginView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = LoginService()

    def post(self, request: HttpRequest):
        data = json.loads(request.body)
        login_info = LoginInfo(**data)
        try:
            access_token = self.service.authenticate(login_info)
        except MemberNotFoundException:
            return JsonResponse(data={}, status=HTTPStatus.NOT_FOUND)
        except IncorrectPasswordException:
            return JsonResponse(data={}, status=HTTPStatus.UNAUTHORIZED)

        return JsonResponse(
            data={
                "access_token": access_token
            },
            status=HTTPStatus.OK
        )
