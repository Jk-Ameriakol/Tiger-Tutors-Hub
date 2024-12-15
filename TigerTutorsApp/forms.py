from django import forms
from .models import Discover, TeamMember, Contact
from django.contrib.auth.models import User
from .models import Profile



class DiscoverUploadForm(forms.ModelForm):
    class Meta:
        model = Discover
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


from django import forms

class UnifiedDocumentForm(forms.Form):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'class': 'form-control'}))
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    SUBJECT_CHOICES = [
        ('mathematics', 'Mathematics'),
        ('physics', 'Physics'),
        ('computer', 'Computer'),
    ]
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))



from django import forms
from .models import TeamMember


class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'role', 'image', 'facebook', 'twitter', 'instagram', 'linkedin']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control w-75 d-inline-block'}),
            'role': forms.TextInput(attrs={'class': 'form-control w-75 d-inline-block'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file w-75 d-inline-block'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control w-75 d-inline-block'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control w-75 d-inline-block'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control w-75 d-inline-block'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control w-75 d-inline-block'}),
        }



class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }



#user registration
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password']


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'email', 'bio', 'location']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }
