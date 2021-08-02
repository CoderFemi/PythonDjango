from django.shortcuts import render, redirect
from .models import Project
from .forms import ProjectForm

def projects(request):
    projects = Project.objects.all()
    context = {'projects': projects}
    return render(request, 'projects/projects.html', context)


def show_project(request, param):
    project = Project.objects.get(id=param)
    context = {'project': project}
    return render(request, 'projects/show_project.html', context)


def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projects')

    form = ProjectForm()
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


def update_project(request, param):
    project = Project.objects.get(id=param)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')

    form = ProjectForm(instance=project)
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


def delete_project(request, param):
    project = Project.objects.get(id=param)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object': project}
    return render(request, 'projects/delete_template.html', context)