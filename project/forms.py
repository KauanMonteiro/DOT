from django.forms import ModelForm,DateInput,Textarea,ValidationError
from .models import Project,Task,MemberProject,Sprint

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name','description']

    def __init__(self,*args, user=None, **kwargs):
        super().__init__(*args,**kwargs)
        self.user = user
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')
        if not name:
            self.add_error('name', 'Name is required.')
        if not description:
            self.add_error('description', 'Description is required.')
        return cleaned_data

    def save(self, commit = True):
        project = super().save(commit=False)
        project.owner = self.user
        if commit:
            project.save()
        return project

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "priority", "sprint", "assignee", "deadline"]
        widgets = {
            "deadline": DateInput(attrs={"type": "date"}),
            "description": Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, project=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.project = project
        if project is not None:
            self.fields["sprint"].queryset = Sprint.objects.filter(project=project)
            self.fields["sprint"].required = False

            member_ids = project.memberships.values_list("member_id", flat=True)
            self.fields["assignee"].queryset = self.fields["assignee"].queryset.filter(
                id__in=list(member_ids) + [project.owner_id]
            )
            self.fields["assignee"].required = False


class SprintForm(ModelForm):
    class Meta:
        model = Sprint
        fields = ["name", "start_date", "end_date"]
        widgets = {
            "start_date": DateInput(attrs={"type": "date"}),
            "end_date": DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")
        if start and end and end <= start:
            raise ValidationError("A data de término deve ser posterior à data de início.")
        return cleaned_data