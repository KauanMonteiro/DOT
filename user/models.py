from django.contrib.auth.models import AbstractUser
from django.db import models
from project.models import Project
import random
import string

class User(AbstractUser):
    code = models.CharField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self._generate_unique_code()
        super().save(*args, **kwargs)

    def _generate_unique_code(self):
        while True:
            code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not User.objects.filter(code=code).exists():
                return code