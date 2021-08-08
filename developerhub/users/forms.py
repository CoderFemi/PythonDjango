from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Skill, Message

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']
        labels = {
            'first_name': 'Name'
        }


    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for (name, field) in self.fields.items():
            field.widget.attrs.update({'class':'input'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']


    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for (name, field) in self.fields.items():
            field.widget.attrs.update({'class':'input'})


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        exclude = ['owner']


    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for (name, field) in self.fields.items():
            field.widget.attrs.update({'class':'input'})


class MessageForm(ModelForm):
    class Meta:
        model = Message
        exclude = ['is_read']


    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for (name, field) in self.fields.items():
            field.widget.attrs.update({'class':'input'})