from django.contrib.auth.base_user import  AbstractBaseUser
from django.db import models

# Create your models here.

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)