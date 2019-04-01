from django.urls import path
from .views import (
    HomeView,
    RegisterView,
    RegisterHoursView,
    RegisterHourDetailView,
    RegPageListViewSuperUser,
)


urlpatterns = [
    path('', HomeView.as_view(), name='home_page'),
    path('register/<slug:month>/<int:year>/', RegisterView.as_view(), name='register_page'),
    path('register/<slug:month>/<int:year>/<int:day>', RegisterHoursView.as_view(), name='register_hours'),
    path('register/<slug:month>/<int:year>/<int:day>/<int:hour>', RegisterHourDetailView.as_view(), name='register_hours_detail'),
    path('list', RegPageListViewSuperUser.as_view(), name='list_view'),
    ]

