from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Notes(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    descriptions=models.TextField()

    def __str__(self):
        return self.title
    

class HomeWork(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    subject=models.CharField(max_length=100)
    title=models.CharField(max_length=100)
    descriptions=models.TextField()
    due=models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    # is_finished=models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    
class Todo(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')

    def __str__(self):
        return self.title

class Register(models.Model):
    user=user=models.ForeignKey(User,on_delete=models.CASCADE)