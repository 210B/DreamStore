from django.urls import path
from . import views

urlpatterns = [
    path('', views.DreamList.as_view()),
    path('<int:pk>/', views.DreamDetail.as_view())
]