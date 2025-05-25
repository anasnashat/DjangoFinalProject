from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Reply
from .forms import ReplyForm
from comments.models import Comment

@login_required
@require_POST
def add_reply(request, comment_id):
    """Add a new reply to a comment"""
    comment = get_object_or_404(Comment, id=comment_id)
    form = ReplyForm(request.POST)
    
    if form.is_valid():
        reply = form.save(commit=False)
        reply.user = request.user
        reply.comment = comment
        reply.save()
        messages.success(request, 'Your reply has been added successfully!')
        return redirect('project-detail', slug=comment.project.slug)

    else:
        messages.error(request, 'There was an error adding your reply.')
        return redirect('project-detail', project_id=comment.project.id)

@login_required
def edit_reply(request, reply_id):
    """Edit an existing reply"""
    reply = get_object_or_404(Reply, id=reply_id, user=request.user)
    
    if request.method == 'POST':
        form = ReplyForm(request.POST, instance=reply)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your reply has been updated successfully!')
            return redirect('project-detail', slug=reply.comment.project.slug)

    else:
        form = ReplyForm(instance=reply)
    
    context = {
        'form': form,
        'reply': reply,
        'comment': reply.comment,
        'project': reply.comment.project
    }
    return render(request, 'replays/edit_reply.html', context)

@login_required
def delete_reply(request, reply_id):
    """Delete a reply"""
    reply = get_object_or_404(Reply, id=reply_id, user=request.user)
    project_id = reply.comment.project.id
    
    if request.method == 'POST':
        reply.delete()
        messages.success(request, 'Your reply has been deleted successfully!')
        return redirect('project-detail', slug=reply.comment.project.slug)

    
    context = {
        'reply': reply,
        'comment': reply.comment,
        'project': reply.comment.project
    }
    return render(request, 'replays/delete_reply.html', context)

def get_comment_replies(request, comment_id):
    """Get replies for a comment (for AJAX requests)"""
    comment = get_object_or_404(Comment, id=comment_id)
    replies = Reply.objects.filter(comment=comment).select_related('user').order_by('created_at')
    
    replies_data = []
    for reply in replies:
        replies_data.append({
            'id': reply.id,
            'content': reply.replay,
            'user': reply.user.get_full_name() or reply.user.username,
            'created_at': reply.created_at.strftime('%B %d, %Y at %I:%M %p'),
            'can_edit': reply.user == request.user if request.user.is_authenticated else False
        })
    
    return JsonResponse({'replies': replies_data})