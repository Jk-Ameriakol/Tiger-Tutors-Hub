import json
import logging

import openai
import requests
from PyPDF2 import PdfReader
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from requests.auth import HTTPBasicAuth

from .credentials import MpesaAccessToken, LipanaMpesaPpassword
from .models import Discover, Contact, Member, MathematicsDocument, PhysicsDocument, ComputerDocument, TeamMember
from .forms import DiscoverUploadForm, UnifiedDocumentForm, DocumentForm, TeamMemberForm, ContactForm
from docx import Document as DocxDocument

# Create your views here.
def starter(request):
    return render(request,'starter-page.html')

def index(request):
    if request.method=='POST':
        if Member.objects.filter(
                username=request.POST['username'],
                password=request.POST['password'] ).exists():
             members = Member.objects.get(
                 username=request.POST['username'],
                 password=request.POST['password'])
             return render(request,'index.html',{'members':members})
        else:
             return render(request,'login.html')
    else:
        return render(request,'index.html')



def about(request):
    return render(request,'about.html')

def services(request):
    return render(request,'services.html')


def membership(request):
    return render(request, 'membership.html')

def team(request):
    team_members = TeamMember.objects.all()
    return render(request, 'team.html', {'team_members': team_members})


def team_upload(request):
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/team')
    else:
        form = TeamMemberForm()
    return render(request, 'team_upload.html', {'form': form})


def contact(request):
    if request.method == 'POST':
        contacts = Contact(name=request.POST['name'],
                      email=request.POST['email'],
                      subject=request.POST['subject'],
                      message=request.POST['message']
                      )
        contacts.save()
        return redirect('/contact')
    else:
        return render(request, 'contact.html')


def discover_upload(request):
    if request.method == 'POST':
        form = DiscoverUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = DiscoverUploadForm()
    return render(request, 'discover.html', {'form': form})


def landing(request):
    images = Discover.objects.all()  # Ensure this returns a QuerySet
    return render(request, 'landing-page.html', {'images': images})


from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Ensure the user argument is passed here
                return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})




def upload_document(request):
    if request.method == 'POST':
        form = UnifiedDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            image = form.cleaned_data['image']
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            file = form.cleaned_data['file']

            if subject == 'mathematics':
                MathematicsDocument.objects.create(image=image, title=title, description=description, file=file)
            elif subject == 'physics':
                PhysicsDocument.objects.create(image=image, title=title, description=description, file=file)
            elif subject == 'computer':
                ComputerDocument.objects.create(image=image, title=title, description=description, file=file)

            return redirect('upload_document')
    else:
        form = UnifiedDocumentForm()
    return render(request, 'upload_document.html', {'form': form})




def subject_documents(request):
    math_docs = MathematicsDocument.objects.all()
    physics_docs = PhysicsDocument.objects.all()
    computer_docs = ComputerDocument.objects.all()
    context = {
        'math_docs': math_docs,
        'physics_docs': physics_docs,
        'computer_docs': computer_docs,
    }
    return render(request, 'subject_documents.html', context)


def view_pdf(request, subject, document_id):
    if subject == 'mathematics':
        document = get_object_or_404(MathematicsDocument, id=document_id)
    elif subject == 'physics':
        document = get_object_or_404(PhysicsDocument, id=document_id)
    elif subject == 'computer':
        document = get_object_or_404(ComputerDocument, id=document_id)
    else:
        document = None

    context = {
        'document_name': document.title if document else '',
        'file_path': document.file.url if document else '',
    }
    return render(request, 'view_pdf.html', context)


def about_more(request):
    return render(request,'about_more.html')

def service_details(request):
    return render(request,'service-details.html')

def terms(request):
    return render(request,'terms.html')



def token(request):
    consumer_key = 'xas799P0Mqi2lJXmXmhEUnc4gPeL4tsSxOS8e8PwMdk25Jdg'
    consumer_secret = '0PHtJT7MGwOIX0aCHoXgZw9kxluDAbAxXq4ehZlgMffecV5vlcNnGVSnf3iQwvMe'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})

def pay(request):
   return render(request, 'pay.html')



def stk(request):
    if request.method =="POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "TigerTutorsHub",
            "TransactionDesc": "Web Development Charges"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse("Success")





def contact_list(request):
    contacts = Contact.objects.all()
    return render(request, 'contact_list.html', {'contacts': contacts})

def edit_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contact_list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'edit_contact.html', {'form': form})

def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('contact_list')
    return render(request, 'delete_contact.html', {'contact': contact})



def team_list(request):
    team_members = TeamMember.objects.all()
    return render(request, 'show_team.html', {'team_members': team_members})

def edit_team_member(request, pk):
    team_member = get_object_or_404(TeamMember, pk=pk)
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES, instance=team_member)
        if form.is_valid():
            form.save()
            return redirect('team_list')
    else:
        form = TeamMemberForm(instance=team_member)
    return render(request, 'edit_team_member.html', {'form': form})

def delete_team_member(request, pk):
    team_member = get_object_or_404(TeamMember, pk=pk)
    if request.method == 'POST':
        team_member.delete()
        return redirect('team_list')
    return render(request, 'delete_team_member.html', {'team_member': team_member})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, ProfileUpdateForm
from .models import Member

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Member

@login_required
def profile_view(request):
    member = Member.objects.get(username=request.user.username)
    return render(request, 'profile.html', {'member': member})


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})


def admin_dashboard(request):
    return render(request,'dashboard.html')
