import json
from http import HTTPStatus

from django.http import JsonResponse
from django.views import View

from .dto.signup_info import SignUpInfo
from .exceptions import MemberNotFoundException, DuplicatedIdException
from .service import MemberService


class SignUpView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = MemberService()

    def post(self, request):
        data = json.loads(request.body)
        signup_info = SignUpInfo(**data)
        try:
            self.service.add_member(signup_info)
        except DuplicatedIdException:
            return JsonResponse(data={}, status=HTTPStatus.CONFLICT)
        return JsonResponse(data={}, status=HTTPStatus.CREATED)
