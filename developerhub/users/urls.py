from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('', views.profiles, name='profiles'),
    path('profiles/<str:param>/', views.show_profile, name='show_profile'),
    path('account/', views.user_account, name='account'),
    path('account-edit', views.edit_account, name='edit_account'),
    path('add-skill/', views.add_skill, name='add_skill'),
    path('update-skill/<str:param>/', views.update_skill, name='update_skill'),
    path('delete-skill/<str:param>/', views.delete_skill, name='delete_skill'),
    path('inbox/', views.inbox, name='inbox'),
    path('view-message/<str:param>/', views.view_message, name='message')
]