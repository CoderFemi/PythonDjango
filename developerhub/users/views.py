from django.contrib import auth
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Profile, Skill, Message
from .forms import RegisterForm, ProfileForm, SkillForm, MessageForm
from .utils import paginate_profiles, search_profiles


def register_user(request):
    page = 'register'

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # Get user object and make changes before saving
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('edit_account')
        else:
            messages.error(request, 'An error occurred.')
    else:
        form = RegisterForm()
    
    context = {'page': page, 'form': form}
    return render(request, 'users/auth.html', context)


def login_user(request):
    page = 'login'
    context = {'page': page}

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, {username}!')
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'Invalid credentials.')

    return render(request, 'users/auth.html', context)


def logout_user(request):
    logout(request)
    messages.info(request, 'Goodbye!')
    return redirect('/')


def profiles(request):
    queried_profiles, search_query = search_profiles(request)
    custom_range, paginated_profiles, paginator = paginate_profiles(request, queried_profiles, 3)
    context = {
        'profiles': paginated_profiles, 
        'search_query': search_query,
        'custom_range': custom_range,
        'paginator': paginator
    }
    return render(request, 'users/profiles.html', context)


def show_profile(request, param):
    profile = Profile.objects.get(id=param)
    context = {'profile': profile}
    return render(request, 'users/show_profile.html', context)


@login_required(login_url='login')
def user_account(request):
    profile = request.user.profile
    skills = profile.skill_set.all
    projects = profile.project_set.all()
    context = {'profile': profile, 'skills': skills, 'projects': projects}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    
    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def add_skill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)

        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'A new skill has been added')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def update_skill(request, param):
    profile = request.user.profile
    skill = profile.skill_set.get(id=param)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)

        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def delete_skill(request, param):
    profile = request.user.profile
    skill = profile.skill_set.get(id=param)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill deleted.')
        return redirect('account')
        
    context = {'object': skill}
    return render(request, 'delete_template.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    message_requests = profile.messages.all()
    unread_count = message_requests.filter(is_read=False).count()
    context = {'message_requests': message_requests, 'unread_count': unread_count}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def view_message(request, param):
    profile = request.user.profile
    message = profile.messages.get(id=param)

    if message.is_read == False:
        message.is_read = True
        message.save()
        
    context = {'message': message}
    return render(request, 'users/message.html', context)


def compose_message(request, param):
    recipient = Profile.objects.get(id=param)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid:
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()
            messages.success(request, 'Message sent!')
            return redirect('show_profile', param=recipient.id)

    context = {'form': form, 'recipient': recipient}
    return render(request, 'users/message_form.html', context)
