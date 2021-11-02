from http import HTTPStatus

from django.http import JsonResponse
from django.views import View

from .dto.post_content import PostContents
from .service import PostService
from security.service import authorize


class PostView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.post_service = PostService()

    @authorize
    def post(self, request, member):
        data = json.loads(request.body)
        post_contents = PostContents(**data)
        self.post_service.write(post_contents, member)
        return JsonResponse(data={'message': 'SUCCESS'}, status=HTTPStatus.CREATED)
