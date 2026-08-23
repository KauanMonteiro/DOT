from django.shortcuts import render
from .models import Project
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    projects = Project.objects.filter(
        Q(owner=request.user) | Q(memberproject__member=request.user)
    ).distinct()
    return render(request,'pages/home.html',{'projects':projects})
