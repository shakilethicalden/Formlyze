from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.conf import settings
# Create your models here.

role_choices= [
    ('admin', 'Admin'),
    ('patient', 'Patient')
]

form_type=[
    ('appointment', 'Appointment'),
    ('referral', 'Referral'),
    ('employment', 'Employment')
]

class User(AbstractUser):
    username=models.CharField(max_length=20,unique=True)
    email=models.EmailField(unique=True)
    role=models.CharField(max_length=10,choices=role_choices, default='patient')
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS=['username']
    
    def __str__(self):
        return self.username
    
    
class HealthCare(models.Model):
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=200)
    phone=models.CharField(max_length=15)
    email=models.EmailField(blank=True, null=True)
    
    def __str__(self):
        return self.name

    