from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Report
from .forms import ReportForm
from projects.models import Project
from comments.models import Comment

@login_required
def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        content_type = request.POST.get('content_type')
        object_id = request.POST.get('object_id')
        cancel_url = request.POST.get('cancel_url', '/')
        
        try:
            if content_type == 'project':
                content_object = get_object_or_404(Project, id=object_id)
                if not hasattr(content_object, 'created_by'):
                    messages.error(request, "This project has no owner information")
                    return redirect(cancel_url)
                if request.user == content_object.created_by:
                    messages.error(request, "You cannot report your own project")
                    return redirect(cancel_url)
                existing_report = Report.objects.filter(user=request.user, project=content_object).first()
                if existing_report:
                    messages.error(request, "You have already reported this project")
                    return redirect(cancel_url)    
            elif content_type == 'comment':
                content_object = get_object_or_404(Comment, id=object_id)
                if not hasattr(content_object, 'user'):
                    messages.error(request, "This comment has no owner information")
                    return redirect(cancel_url)
                if request.user == content_object.user:
                    messages.error(request, "You cannot report your own comment")
                    return redirect(cancel_url)
                existing_report = Report.objects.filter(user=request.user, comment=content_object).first()
                if existing_report:
                    messages.error(request, "You have already reported this comment")
                    return redirect(cancel_url)
                    
            else:
                messages.error(request, "Invalid content type")
                return redirect(cancel_url)
            
            if form.is_valid():
                report = form.save(commit=False)
                report.user = request.user
                setattr(report, content_type, content_object)
                report.save()
                return render(request, 'reports/report_success.html', {
                    'content_type': content_type,
                    'return_url': cancel_url
                })
            
        except Exception as e:
            messages.error(request, f"Error submitting report: {str(e)}")
            return redirect(cancel_url)
    
    return redirect('home')

def report_list(request):
    if not request.user.is_staff:
        return redirect('home')
    
    reports = Report.objects.all().order_by('-created_at')
    return render(request, 'reports/report_list.html', {'reports': reports})