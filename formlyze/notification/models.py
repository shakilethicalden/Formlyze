from django.db import models
from form.models import Form
# Create your models here.
class NotificationModel(models.Model):
    user_email=models.EmailField(null=True, blank=True)
    message=models.TextField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    read=models.BooleanField(default=False)
    
    
    def save(self,*args, **kwargs):
        if self.read:
            self.delete()
        else:
            return super().save(*args,**kwargs)
        
    def __str__(self):
        return f"Notification for {self.user_email}"
        
        
            