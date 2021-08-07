from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm
from .utils import paginate_projects, search_projects

def projects(request):
    queried_projects, search_query = search_projects(request)
    custom_range, paginated_projects, paginator = paginate_projects(request, queried_projects, 3)

    context = {
        'projects': paginated_projects, 
        'search_query': search_query,
        'paginator': paginator,
        'custom_range': custom_range
    }

    return render(request, 'projects/projects.html', context)


def show_project(request, param):
    project = Project.objects.get(id=param)
    context = {'project': project}
    return render(request, 'projects/show_project.html', context)


@login_required(login_url='login')
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def update_project(request, param):
    profile = request.user.profile
    project = profile.project_set.get(id=param)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def delete_project(request, param):
    profile = request.user.profile
    project = profile.project_set.get(id=param)

    if request.method == 'POST':
        project.delete()
        return redirect('account')
        
    context = {'object': project}
    return render(request, 'delete_template.html', context)