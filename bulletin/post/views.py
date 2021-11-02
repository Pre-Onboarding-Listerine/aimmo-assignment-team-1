import json
from http import HTTPStatus

from django.http import JsonResponse
from django.views import View

from .dto.deleted_post_id import DeletedPostId
from .dto.post_changes import PostChanges
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

    @authorize
    def patch(self, request, member):
        data = json.loads(request.body)
        post_changes = PostChanges(**data)
        self.post_service.edit(post_changes, member)
        return JsonResponse(data={}, status=HTTPStatus.OK)

    @authorize
    def delete(self, request, member):
        data = json.loads(request.body)
        deleted_post_id = DeletedPostId(**data)
        self.post_service.remove(deleted_post_id, member)
        return JsonResponse(data={}, status=HTTPStatus.NO_CONTENT)

    def get(self, request, post_id):
        post_details = self.post_service.details(post_id)
        return JsonResponse(data=post_details.to_dict(), status=HTTPStatus.OK)


class PostListView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.post_service = PostService()

    def get(self, request):
        limit = int(request.GET.get("limit", 10))
        offset = int(request.GET.get("offset", 0))
        postings = self.post_service.list(offset, limit)
        return JsonResponse(data=postings.to_dict(), status=HTTPStatus.OK)

