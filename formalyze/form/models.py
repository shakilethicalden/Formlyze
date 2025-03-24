from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

role_choices= [
    ('admin', 'Admin'),
    ('patient', 'Patient')
]

class User(AbstractUser):
    username=models.CharField(max_length=20,unique=True)
    email=models.EmailField(unique=True)
    role=models.CharField(max_length=10,choices=role_choices, default='patient')
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS=['username']
    
    def __str__(self):
        return self.username
    
    
