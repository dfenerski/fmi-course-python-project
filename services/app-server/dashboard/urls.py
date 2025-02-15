from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('<int:tracker_id>/symbols', login_required(views.DashboardSymbols.as_view()))
]
