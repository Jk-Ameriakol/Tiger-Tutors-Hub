from django import forms

from .models import Discover, Document, TeamMember


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
        fields = ['name', 'role', 'image']

