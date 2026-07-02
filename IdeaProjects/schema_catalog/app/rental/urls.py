from django.urls import path

from .views import RentalView, CalendarView

urlpatterns = [
    path("rental/", RentalView.as_view()),
    path("rental/<int:pk>/", RentalView.as_view()),
    path("rental/calendar/<int:device_id>/", CalendarView.as_view()),
]