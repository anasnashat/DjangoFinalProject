from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from projects.models import Project
from projects.forms import ProjectForm
from django.forms import modelformset_factory
from .forms import ProjectForm, ProjectImageFormSet
from projects.models import ProjectImage

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    ordering = ['-created_at']
    paginate_by = 10


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'projects/project_create.html'
    form_class = ProjectForm
    success_url = reverse_lazy('project-list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['images'] = ProjectImageFormSet(self.request.POST, self.request.FILES, queryset=ProjectImage.objects.none())
        else:
            data['images'] = ProjectImageFormSet(queryset=ProjectImage.objects.none())
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        images = context['images']
        
        project = form.save(commit=False)
        project.created_by = self.request.user
        project.save()
        
        if images.is_valid():
            images.instance = project
            images.save()
        
        return super().form_valid(form)


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'
    slug_url_kwarg = 'slug'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get comments with pagination
        comments_list = Comment.objects.filter(
            project=self.object
        ).select_related('user').prefetch_related(
            'reply_set__user'
        ).order_by('-created_at')
        
        # Pagination for comments
        paginator = Paginator(comments_list, 10)
        page_number = self.request.GET.get('page')
        comments = paginator.get_page(page_number)
        
        # Forms for adding comments and replies
        context['comments'] = comments
        context['comment_form'] = CommentForm()
        context['reply_form'] = ReplyForm()
        
        # Get similar projects based on tags (limit to 4)
        if hasattr(self.object, 'tags') and self.object.tags.exists():
            context['similar_projects'] = Project.objects.filter(
                tags__in=self.object.tags.all()
            ).exclude(id=self.object.id).distinct()[:4]
        
        return context

class ProjectUpdateView(UpdateView):
    model = Project
    template_name = 'projects/project_update.html'
    context_object_name = 'project'
    form_class = ProjectForm
    slug_url_kwarg = 'slug'
    
    def get_success_url(self):
        return reverse_lazy('project-detail', kwargs={'slug': self.object.slug})

class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'projects/project_delete.html'
    success_url = reverse_lazy('project-list')
    slug_url_kwarg = 'slug'




