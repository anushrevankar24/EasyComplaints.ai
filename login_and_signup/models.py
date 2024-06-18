from django.db import models
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):
    phone_number= models.CharField(max_length=15)
    role=models.CharField(max_length=100,default='default_role')
    staff_id = models.CharField(max_length=50,default='default_id')
    def __str__(self):
        return self.username
# Create your models here.
