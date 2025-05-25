from django import template
from django.db.models import Avg
from ratings.models import Rating

register = template.Library()

@register.simple_tag
def get_average_rating(project):
    """Get average rating for a project"""
    avg_rating = Rating.objects.filter(project=project).aggregate(
        Avg('rating')
    )['rating__avg']
    return round(avg_rating, 1) if avg_rating else 0

@register.simple_tag
def get_total_ratings(project):
    """Get total number of ratings for a project"""
    return Rating.objects.filter(project=project).count()

@register.simple_tag
def get_user_rating(project, user):
    """Get user's rating for a project"""
    if not user.is_authenticated:
        return 0
    
    rating = Rating.objects.filter(project=project, user=user).first()
    return rating.rating if rating else 0

@register.simple_tag
def star_range():
    """Return range of 5 for star ratings"""
    return range(1, 6)