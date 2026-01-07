from django.urls import path
from .views import DummyAPI

urlpatterns = [
    path("dummy/", DummyAPI.as_view()),
    path("dummy/<str:kind>/", DummyAPI.as_view()),
]
