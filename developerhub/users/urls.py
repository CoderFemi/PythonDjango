from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles, name='profiles'),
    path('profiles/<str:param>/', views.show_profile, name='show_profile')
]