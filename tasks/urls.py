"""
URL configuration for tasks app.
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("api/tasks/", views.api_tasks),
    path("api/tasks/today-count/", views.api_today_count),
    path("api/tasks/create/", views.api_task_create),
    path("api/tasks/<int:task_id>/", views.api_task_update),
    path("api/tasks/<int:task_id>/delete/", views.api_task_delete),
]
