import json
from http import HTTPStatus

from django.http import JsonResponse, HttpRequest
from django.views import View

from .dto.login_info import LoginInfo
from .service import LoginService


class LoginView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = LoginService()

    def post(self, request: HttpRequest):
        data = json.loads(request.body)
        login_info = LoginInfo(**data)
        access_token = self.service.authenticate(login_info)
        return JsonResponse(
            data={
                "access_token": access_token
            },
            status=HTTPStatus.OK
        )
