from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/<int:taskId>/delete/', views.delete_task, name='delete_task'),
    path('tasks/<int:taskId>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),

]