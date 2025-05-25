
from django.db import models


class Report(models.Model):
    REASON_CHOICES = [
        ('spam', 'Spam or misleading'),
        ('abuse', 'Abusive content'),
        ('scam', 'Scam or fraud'),
        ('other', 'Other'),
    ]
    
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    description = models.TextField(blank=True, null=True)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='reports_made')
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, null=True, blank=True, related_name='reports')
    comment = models.ForeignKey('comments.Comment', on_delete=models.CASCADE, null=True, blank=True, related_name='reports')

    def __str__(self):
        return f"Report #{self.id} - {self.get_reason_display()}"