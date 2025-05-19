from django.db import models

# Create your models here.
class Reply(models.Model):
    replay = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    comment = models.ForeignKey('comments.Comment', on_delete=models.CASCADE)

    def __str__(self):
        return self.replay