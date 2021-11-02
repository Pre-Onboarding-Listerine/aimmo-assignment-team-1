from http import HTTPStatus

from django.http import JsonResponse
from django.views import View

from security.service import AuthorizationService


class PostView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.post_service = PostService()

    @AuthorizationService
    def post(self, request):
        # self.post_service.write(post_contents)
        return JsonResponse(data={}, status=HTTPStatus.CREATED)





