from django.contrib import auth
from django.db import models
from payments.models import Payment
# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    details = models.TextField(blank=True)
    total_target = models.IntegerField(default=0)
    starting_date = models.DateField()
    ending_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    category = models.ForeignKey('categories.Category', on_delete=models.CASCADE)
    tags = models.ManyToManyField('tags.Tag')
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title
        
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    @property
    def amount_raised(self):
        return Payment.objects.filter(project=self, status='succeeded').aggregate(total=models.Sum('amount'))['total'] or 0

    @property
    def progress_percentage(self):
        if self.total_target == 0:
            return 0
        return round((self.amount_raised / self.total_target) * 100, 2)
    


class ProjectImage(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='project_pics')

    def __str__(self):
        return f"Image for {self.project.title}"