from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .models import Rating
from projects.models import Project
import json 

@login_required
def add_rating(request, project_id):
    if request.method == 'POST':
        try:
            # Fetch project and verify user is not the owner
            project = Project.objects.get(id=project_id)
            if project.created_by == request.user:
                return JsonResponse({'success': False, 'message': 'You cannot rate your own project.'})

            data = json.loads(request.body)
            rating = int(data.get('rating'))
            if rating < 1 or rating > 5:
                return JsonResponse({'success': False, 'message': 'Rating must be between 1 and 5'})
            
            rating_obj, created = Rating.objects.get_or_create(
                user=request.user,
                project=project,
                defaults={'rating': rating}
            )

            if not created:
                rating_obj.rating = rating
                rating_obj.save()
            
            ratings = Rating.objects.filter(project=project)
            average = ratings.aggregate(Avg('rating'))['rating__avg'] or 0
            total = ratings.count()

            return JsonResponse({
                'success': True,
                'message': 'Rating submitted successfully',
                'average_rating': round(float(average), 1),
                'total_ratings': total,
                'user_rating': rating
            })

        except Project.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Project not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request'})


def get_project_ratings(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        ratings = Rating.objects.filter(project=project)
        average = ratings.aggregate(Avg('rating'))['rating__avg'] or 0
        total = ratings.count()

        user_rating = None

        if request.user.is_authenticated:
            try:
                user_rating = ratings.get(user=request.user).rating
            except Rating.DoesNotExist:
                pass

        return JsonResponse({
            'average_rating': round(float(average), 1),
            'total_ratings': total,
            'user_rating': user_rating
        })

    except Project.DoesNotExist:
        return JsonResponse({'average_rating': 0, 'total_ratings': 0, 'user_rating': None})