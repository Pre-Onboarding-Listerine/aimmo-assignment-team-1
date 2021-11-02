import json
from http import HTTPStatus

from django.http import JsonResponse
from django.views import View

from .dto.signup_info import SignUpInfo
from .service import MemberService


class SignUpView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = MemberService()

    def post(self, request):
        data = json.loads(request.body)
        signup_info = SignUpInfo(**data)
        self.service.add_member(signup_info)
        return JsonResponse(data={}, status=HTTPStatus.CREATED)
