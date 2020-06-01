from django.urls import path
from .views import EmailDataAPIView

urlpatterns = [
    path('', EmailDataAPIView.as_view()),
]
