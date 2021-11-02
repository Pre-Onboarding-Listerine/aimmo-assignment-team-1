from django.urls import path

from .views import PostView

urlpatterns = [
    path("", PostView.as_view()),
    path("/<int:post_id>", PostView.as_view()),
]
