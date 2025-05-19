from django.contrib import auth
from django.db import models

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='project_pics')
    details = models.TextField(blank=True)
    total_target = models.IntegerField(default=0)
    starting_date = models.DateField()
    ending_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    category = models.ForeignKey('categories.Category', on_delete=models.CASCADE)
    tags = models.ManyToManyField('tags.Tag')
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

