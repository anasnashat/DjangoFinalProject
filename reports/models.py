from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.

class Report(models.Model):
    reason = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey('comments.Comment', on_delete=models.CASCADE, null=True, blank=True)
    replay = models.ForeignKey('replays.Reply', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.reason

    def clean(self):
        super().clean()
        entities = [bool(self.project), bool(self.comment), bool(self.replay)]
        if sum(entities) != 1:
            raise ValidationError(
                "A report must reference exactly one of: project or comment"
            )

        if self.is_resolved and not self.reason:
            raise ValidationError({'reason': 'This field is required.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


