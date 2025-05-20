from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from projects.models import Project
from projects.forms import ProjectForm


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    ordering = ['-created_at']
    paginate_by = 10


class ProjectCreateView(CreateView):
    model = Project
    template_name = 'projects/project_create.html'
    form_class = ProjectForm
    success_url = reverse_lazy('project-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'
    slug_url_kwarg = 'slug'

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




