from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
import uuid
from django.conf import settings
# Create your models here.



form_type=[
    ('appointment', 'Appointment'),
    ('referral', 'Referral'),
    ('employment', 'Employment')
]

class User(AbstractUser):
    username=models.CharField(max_length=20,unique=True)
    email=models.EmailField(unique=True)
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS=['username']
    
    groups = models.ManyToManyField(Group, related_name="custom_user_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions")
    
    
    
    def __str__(self):
        return self.username
    
    
class HealthCare(models.Model):
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
    form_type=models.CharField(max_length=20,choices=form_type)
    created_by=models.ForeignKey(User, on_delete=models.CASCADE)
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
    