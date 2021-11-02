import json
from http import HTTPStatus

from django.http import JsonResponse
from django.views import View

from .dto.deleted_post_id import DeletedPostId
from .dto.list_params import ListParams
from .dto.post_changes import PostChanges
from .dto.post_content import PostContents
from .service import PostService
from security.service import authorize, general_authorize


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

    @general_authorize
    def get(self, request, member, post_id):
        post_details = self.post_service.details(post_id, member)
        return JsonResponse(data=post_details.to_dict(), status=HTTPStatus.OK)


class PostListView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.post_service = PostService()

    def get(self, request):
        limit = int(request.GET.get("limit", 10))
        offset = int(request.GET.get("offset", 0))
        category = request.GET.get("category", None)
        keyword = request.GET.get("keyword", None)

        params = ListParams(
            limit=limit,
            offset=offset,
            category=category,
            keyword=keyword
        )

        postings = self.post_service.list(params)
        return JsonResponse(data=postings.to_dict(), status=HTTPStatus.OK)

