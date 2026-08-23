from django.forms import ModelForm
from .models import Project

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

    