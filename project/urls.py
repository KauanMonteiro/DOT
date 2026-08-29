from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('registerproject/',views.register_project, name='register_project'),
    path("projects/<int:project_id>/", views.project_detail, name="project_detail"),
    path("projects/<int:project_id>/tasks/add/", views.add_task, name="task_create"),
    path("projects/<int:project_id>/sprints/add/", views.add_sprint, name="sprint_create"),
    path("projects/<int:project_id>/tasks/<int:task_id>/add-to-sprint/", views.add_task_to_sprint, name="task_add_to_sprint"),
    path("projects/<int:project_id>/tasks/<int:task_id>/status/", views.update_task_status, name="task_update_status"),
    path("projects/<int:project_id>/tasks/<int:task_id>/remove-from-sprint/", views.remove_task_from_sprint, name="task_remove_from_sprint"),
    path("projects/<int:project_id>/tasks/<int:task_id>/edit/", views.edit_task, name="task_edit"),
    path("projects/<int:project_id>/sprints/<int:sprint_id>/edit/", views.edit_sprint, name="sprint_edit"),
    path("projects/<int:project_id>/sprints/<int:sprint_id>/delete/", views.delete_sprint, name="sprint_delete"),
    path("projects/<int:project_id>/members/add/", views.add_member, name="member_add"),
    path("projects/<int:project_id>/team/<int:member_id>/delete/", views.delete_member, name="delete_member"),
    path("projects/<int:project_id>/tasks/<int:task_id>/", views.task_detail, name="task_detail"),
    ]
