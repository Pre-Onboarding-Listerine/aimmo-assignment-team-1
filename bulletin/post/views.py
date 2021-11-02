import json
from http import HTTPStatus

from django.http import JsonResponse
from django.views import View

from .dto.deleted_post_id import DeletedPostId
from .dto.list_params import ListParams
from .dto.post_changes import PostChanges
from .dto.post_content import PostContents
from .exceptions import PostNotFoundException
from .service import PostService
from security.service import authorize, general_authorize

from security.exceptions import UnauthorizedException


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
        try:
            self.post_service.edit(post_changes, member)
        except PostNotFoundException:
            return JsonResponse(data={}, status=HTTPStatus.NOT_FOUND)
        except UnauthorizedException:
            return JsonResponse(data={}, status=HTTPStatus.UNAUTHORIZED)
        return JsonResponse(data={}, status=HTTPStatus.OK)

    @authorize
    def delete(self, request, member):
        data = json.loads(request.body)
        deleted_post_id = DeletedPostId(**data)
        try:
            self.post_service.remove(deleted_post_id, member)
        except PostNotFoundException:
            return JsonResponse(data={}, status=HTTPStatus.NOT_FOUND)
        except UnauthorizedException:
            return JsonResponse(data={}, status=HTTPStatus.UNAUTHORIZED)
        return JsonResponse(data={}, status=HTTPStatus.NO_CONTENT)

    @general_authorize
    def get(self, request, member, post_id):
        try:
            post_details = self.post_service.details(post_id, member)
        except PostNotFoundException:
            return JsonResponse(data={}, status=HTTPStatus.NOT_FOUND)
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

