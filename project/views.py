from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from .models import Project
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm,TaskForm,SprintForm
from django.contrib import messages
from .models import Project,Task
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.http import require_POST
@login_required
def home(request):
    projects = Project.objects.filter(
        Q(owner=request.user) | Q(memberships__member=request.user)
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

def _get_owned_or_member_project(request, project_id):
    """Garante que o usuário só acessa projetos que possui ou dos quais é membro."""
    return get_object_or_404(
        Project.objects.filter(
            Q(owner=request.user) | Q(memberships__member=request.user)
        ).distinct(),
        pk=project_id,
    )


def _get_project_as_owner_or_admin(request, project_id):
    """Só retorna o projeto se o usuário for owner ou admin (não membro comum)."""
    return get_object_or_404(
        Project.objects.filter(
            Q(owner=request.user)
            | Q(memberships__member=request.user, memberships__role="admin")
        ).distinct(),
        pk=project_id,
    )


@login_required
def project_detail(request, project_id):
    project = _get_owned_or_member_project(request, project_id)
    sprint = project.sprints.order_by("-start_date").first()

    timeline = None
    if sprint:
        total_days = (sprint.end_date - sprint.start_date).days + 1
        today = timezone.localdate()
        days = [
            {
                "label": (sprint.start_date + timedelta(days=i)).strftime("%d"),
                "is_today": (sprint.start_date + timedelta(days=i)) == today,
            }
            for i in range(total_days)
        ]

        timeline_tasks = []
        for task in sprint.tasks.all():
            if not task.deadline:
                continue
            deadline = max(sprint.start_date, min(task.deadline, sprint.end_date))
            duration = max(1, (deadline - sprint.start_date).days + 1)
            timeline_tasks.append({
                "title": task.title,
                "status": task.status,
                "start_day": 1,
                "duration": duration,
            })

        timeline = {"days": days, "tasks": timeline_tasks}

        sprint.todo_tasks = sprint.tasks.filter(status="todo")
        sprint.in_progress_tasks = sprint.tasks.filter(status="in_progress")
        sprint.done_tasks = sprint.tasks.filter(status="done")
        sprint.total_count = sprint.tasks.count()
        sprint.done_count = sprint.tasks.filter(status="done").count()

    context = {
        "project": project,
        "sprint": sprint,
        "timeline": timeline,
        "backlog_tasks": project.tasks.filter(sprint__isnull=True).order_by("-created_at"),
        "backlog_count": project.tasks.filter(sprint__isnull=True).count(),
        "upcoming_deadline_tasks": project.tasks
            .filter(deadline__isnull=False, deadline__gte=timezone.localdate())
            .exclude(status="done")
            .order_by("deadline")[:6],
    }
    return render(request, "pages/project_detail.html", context)


@login_required
def add_task(request, project_id):
    project = _get_project_as_owner_or_admin(request, project_id)  # só owner ou admin adicionam task

    if request.method == "POST":
        form = TaskForm(request.POST, project=project)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect("project_detail", project_id=project.id)
    else:
        form = TaskForm(project=project)

    return render(request, "pages/form.html", {"form": form, "project": project})


@login_required
def add_sprint(request, project_id):
    project = _get_project_as_owner_or_admin(request, project_id)  # só owner ou admin adicionam sprint

    if request.method == "POST":
        form = SprintForm(request.POST)
        if form.is_valid():
            sprint = form.save(commit=False)
            sprint.project = project
            sprint.save()
            return redirect("project_detail", project_id=project.id)
    else:
        form = SprintForm()

    return render(request, "pages/form.html", {"form": form, "project": project})

@login_required
@require_POST
def add_task_to_sprint(request, project_id, task_id):
    project = _get_owned_or_member_project(request, project_id)
    sprint = project.sprints.order_by("-start_date").first()

    if sprint:
        can_edit_task = (
            Q(assignee=request.user)
            | Q(project__owner=request.user)
            | Q(project__memberships__member=request.user, project__memberships__role="admin")
        )
        task = get_object_or_404(project.tasks.filter(can_edit_task), pk=task_id)
        task.sprint = sprint
        task.save(update_fields=["sprint"])

    return redirect(f"{request.path_info}#backlog")

@login_required
@require_POST
def update_task_status(request, project_id, task_id):
    project = _get_owned_or_member_project(request, project_id)
    can_edit_task = (
        Q(assignee=request.user)
        | Q(project__owner=request.user)
        | Q(project__memberships__member=request.user, project__memberships__role="admin")
    )
    task = get_object_or_404(project.tasks.filter(can_edit_task), pk=task_id)

    return redirect("project_detail", project_id=project.id)


@login_required
@require_POST
def remove_task_from_sprint(request, project_id, task_id):
    project = _get_owned_or_member_project(request, project_id)
    can_edit_task = (
        Q(assignee=request.user)
        | Q(project__owner=request.user)
        | Q(project__memberships__member=request.user, project__memberships__role="admin")
    )
    task = get_object_or_404(project.tasks.filter(can_edit_task), pk=task_id)
    task.sprint = None
    task.save(update_fields=["sprint"])

    return redirect(f"{reverse('project_detail', args=[project.id])}#backlog")