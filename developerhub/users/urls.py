from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('', views.profiles, name='profiles'),
    path('profiles/<str:param>/', views.show_profile, name='show_profile')
]