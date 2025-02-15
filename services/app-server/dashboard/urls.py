from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('<int:tracker_id>/symbols', views.symbols)
]
