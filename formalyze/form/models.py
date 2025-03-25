from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
import uuid
from django.conf import settings
from users.models import CustomUser
# Create your models here.

    
    
class HealthCare(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=200)
    phone=models.CharField(max_length=15)
    email=models.EmailField(blank=True, null=True)
    
    def __str__(self):
        return self.name


class Form(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    image=models.ImageField(upload_to='images/')
    fields=models.JSONField() # it will be store data dynamically 
    is_active=models.BooleanField(default=True)
    created_by=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    """ generate unique token for form we will use it to make unique link"""
    unique_token=models.UUIDField(default=uuid.uuid4, unique=True, editable=False) 
    
    
    def __str__(self):
        return self.title
    

class FormResponse(models.Model):
    form=models.ForeignKey(Form, on_delete=models.CASCADE)
    response_data=models.JSONField() #dynamically store data of submission
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f" Response for {self.form.title}"
    