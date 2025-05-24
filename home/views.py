# from django.shortcuts import get_object_or_404, render
# from projects.models import Project
# from categories.models import Category
# from tags.models import Tag
# from django.db.models import Q
# from django.db.models import Avg




# def homepage(request):
#     top_rated_projects = Project.objects.annotate(
#     avg_rating=Avg('rating__rating')).order_by('-avg_rating')[:5]
#     latest_projects = Project.objects.order_by('-created_at')[:5]
#     featured_projects = Project.objects.filter(is_featured=True)
#     categories = Category.objects.all()

#     context = {
#         'top_projects': top_rated_projects,
#         'latest_projects': latest_projects,
#         'featured_projects': featured_projects,
#         'categories': categories
#     }
#     return render(request, 'home/homepage.html', context)

# # Search by title or tag
# def search(request):
#     query = request.GET.get('q')
#     results = Project.objects.filter(
#         Q(title__icontains=query) |
#         Q(tags__name__icontains=query)
#     ).distinct()
#     return render(request, 'search_results.html', {'results': results})


from django.shortcuts import render
from django.db.models import Avg, Q
from projects.models import Project
from categories.models import Category
from django.shortcuts import get_object_or_404, render

def search_results(request):
    query = request.GET.get('q')
    search_results = Project.objects.filter(title__icontains=query) if query else []
    return render(request, 'home/search_results.html', {'search_results': search_results})

def homepage(request):
    top_rated_projects = Project.objects.annotate(
        avg_rating=Avg('rating__rating')
    ).order_by('-avg_rating')[:5]

    latest_projects = Project.objects.order_by('-created_at')[:5]
    featured_projects = Project.objects.filter(is_featured=True)
    categories = Category.objects.all()
    
    context = {
        'top_projects': top_rated_projects,
        'latest_projects': latest_projects,
        'featured_projects': featured_projects,
        'categories': categories
    }

    return render(request, 'home/homepage.html', context)

# View projects by category
def category_projects(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    projects = Project.objects.filter(category=category)

    return render(request, 'home/category_projects.html', {'category': category, 'projects': projects})
