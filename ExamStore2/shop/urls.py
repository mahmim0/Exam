from django.urls import path, include
from .views import index, chart

urlpatterns = [
    path("", index),
    path("chart/", chart)
]
