from django.db import models

# Create your models here.

class Rating(models.Model):
    rating = models.IntegerField()

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} : {self.rating}"