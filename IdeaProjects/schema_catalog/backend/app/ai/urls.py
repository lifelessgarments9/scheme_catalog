from django.urls import path

from app.ai.views import RecommendationView

urlpatterns = [
    path("recommend/", RecommendationView.as_view()),
]