from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="owned_projects")

    def __str__(self):
        return self.name

class MemberProject(models.Model):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("member", "Member"),
    )

    member = models.ForeignKey("user.User", on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")

    class Meta:
        unique_together = ("member", "project")

    def __str__(self):
        return f"{self.member} in {self.project} ({self.role})"

    