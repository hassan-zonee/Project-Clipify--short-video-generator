from django.urls import path
from . import views

urlpatterns = [
    path('generate-clips/', views.generate_clips),
]
