from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    company = models.TextField(blank=True)
    full_txt = models.TextField('Описания')
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title