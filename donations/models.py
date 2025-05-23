from django.db import models


class Donation(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='pending')
    payment_id = models.ForeignKey('payments.Payment', on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.username} donated {self.amount} to {self.project.title}"