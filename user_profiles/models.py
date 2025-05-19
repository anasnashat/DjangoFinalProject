from django.db import models

# Create your models here.

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    country= models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    facebook_profile = models.URLField(blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')


    def __str__(self):
        return f'{self.user.username} Profile'
