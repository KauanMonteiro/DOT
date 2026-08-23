from django.contrib import admin
from .models import Project,Task,MemberProject,Sprint

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(MemberProject)
admin.site.register(Sprint)
