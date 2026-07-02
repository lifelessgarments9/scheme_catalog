from django.urls import path

from .views import DeviceListView, DeviceDetailView

urlpatterns = [
    path("catalog/", DeviceListView.as_view()),
    path("catalog/<int:pk>/", DeviceDetailView.as_view()),
]