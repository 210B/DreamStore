from django.urls import path
from . import views

urlpatterns = [
    path('', views.DreamList.as_view()),
    path('<int:pk>/', views.DreamDetail.as_view()),
    path('home', views.home_page),
    path('search/<str:q>/', views.DreamSearch.as_view()),
    path('theme/<str:slug>/', views.theme_page),
    path('producer/<str:slug>/', views.producer_page),
    path('update_dream/<int:pk>/', views.DreamUpdate.as_view()),
    path('create_dream/', views.DreamCreate.as_view()),
    path('<int:pk>/new_comment/', views.new_comment),
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()),
]