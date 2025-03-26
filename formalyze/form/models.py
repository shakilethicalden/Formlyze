from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
import uuid
from django.conf import settings
from users.models import User
# Create your models here.

    

class Form(models.Model):
    created_by=models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    description=models.TextField()
    image=models.ImageField(upload_to='images/')
    fields=models.JSONField() # it will be store data dynamically 
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    """ generate unique token for form we will use it to make unique link"""
    unique_token=models.UUIDField(default=uuid.uuid4, unique=True, editable=False) 
    
    def get_form_link(self):
        return f"{settings.FRONTEND_URL}/{self.unique_token}"
    
    def __str__(self):
        return self.title
    

class FormResponse(models.Model):
    form=models.ForeignKey(Form, on_delete=models.CASCADE)
    responder_email=models.EmailField(blank=True,null=True)
    response_data=models.JSONField() #dynamically store data of submission
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f" Response for {self.form.title}"
    