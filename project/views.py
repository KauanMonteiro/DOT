from django.shortcuts import render
from .models import Project
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm
from django.contrib import messages

@login_required
def home(request):
    projects = Project.objects.filter(
        Q(owner=request.user) | Q(memberproject__member=request.user)
    ).distinct()
    return render(request,'pages/home.html',{'projects':projects})

@login_required
def register_project(request):
    form = ProjectForm(request.POST or None, user=request.user)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Projeto cadastrado com sucesso!")
        else:
            messages.error(request, "Erro ao cadastrar o projeto. Verifique os campos informados.")
    return render(request,'pages/form.html',{'form':form})
