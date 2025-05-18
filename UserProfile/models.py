from django.db import models

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    country= models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
