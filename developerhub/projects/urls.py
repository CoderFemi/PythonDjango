from django.urls import path
from . import views
    
urlpatterns = [
    path('', views.projects, name='projects'),
    path('project-new/', views.create_project, name='create_project'),
    path('project-update/<str:param>', views.update_project, name='update_project'),
    path('project-delete/<str:param>', views.delete_project, name='delete_project'),
    path('project-show/<str:param>', views.show_project, name='show_project'),
]