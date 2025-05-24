from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Comment
from .forms import CommentForm
from projects.models import Project

@login_required
@require_POST
def add_comment(request, project_id):
    """Add a new comment to a project"""
    project = get_object_or_404(Project, id=project_id)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.project = project
        comment.save()
        messages.success(request, 'Your comment has been added successfully!')
        return redirect('project-detail', slug=comment.project.slug)

    else:
        messages.error(request, 'There was an error adding your comment.')
        return redirect('project-detail', slug=comment.project.slug)
@login_required
def edit_comment(request, comment_id):
    """Edit an existing comment"""
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your comment has been updated successfully!')
            return redirect('project-detail', slug=comment.project.slug)

    else:
        form = CommentForm(instance=comment)
    
    context = {
        'form': form,
        'comment': comment,
        'project': comment.project
    }
    return render(request, 'comments/edit_comment.html', context)

@login_required
def delete_comment(request, comment_id):
    """Delete a comment"""
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    project_id = comment.project.id
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Your comment has been deleted successfully!')
        return redirect('project-detail', slug=comment.project.slug)
    
    context = {
        'comment': comment,
        'project': comment.project
    }
    return render(request, 'comments/delete_comment.html', context)

def get_project_comments(request, project_id):
    """Get comments for a project (for AJAX requests)"""
    project = get_object_or_404(Project, id=project_id)
    comments = Comment.objects.filter(project=project).select_related('user').order_by('-created_at')
    
    comments_data = []
    for comment in comments:
        comments_data.append({
            'id': comment.id,
            'content': comment.content,
            'user': comment.user.get_full_name() or comment.user.username,
            'created_at': comment.created_at.strftime('%B %d, %Y at %I:%M %p'),
            'can_edit': comment.user == request.user if request.user.is_authenticated else False
        })
    
    return JsonResponse({'comments': comments_data})