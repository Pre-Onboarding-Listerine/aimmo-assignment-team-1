from django.http import JsonResponse
from django.views import View


class LoginView(View):
    def get(self, request):
        return JsonResponse({"asd": "hello django"})
