from django import forms

from .models import Discover, Document, TeamMember, Contact


class DiscoverUploadForm(forms.ModelForm):
    class Meta:
        model = Discover
        fields = ('title', 'description', 'image')

class UnifiedDocumentForm(forms.Form):
    image = forms.ImageField()
    title = forms.CharField(max_length=50)
    description = forms.CharField(max_length=200)
    file = forms.FileField()
    SUBJECT_CHOICES = [
        ('mathematics', 'Mathematics'),
        ('physics', 'Physics'),
        ('computer', 'Computer'),
    ]
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('file',)


class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'role', 'image', 'facebook', 'twitter', 'instagram', 'linkedin']



class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']


from django import forms
from .models import Member

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Member
        fields = ['username', 'password']

from django import forms
from .models import Member

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['image', 'first_name', 'last_name', 'email', 'phone', 'address']

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if field_name == 'image':
                field.widget.attrs.update({'class': 'form-control-file'})






