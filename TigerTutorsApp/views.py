import json
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from requests.auth import HTTPBasicAuth

from .credentials import MpesaAccessToken, LipanaMpesaPpassword
from .models import Discover, Contact, MathematicsDocument, PhysicsDocument, ComputerDocument, TeamMember, Member
from .forms import DiscoverUploadForm, UnifiedDocumentForm, TeamMemberForm, ContactForm
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, ProfileForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


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

def terms(request):
    return render(request,'terms.html')


#Payment and M-Pesa APIs views
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



#Contact views
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


#team members views
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


#User Registration
from django.contrib.auth import login
from django.urls import reverse

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'User registered successfully. Please log in.')
            return redirect(reverse('login'))  # Redirect to the login page
    else:
        form = UserRegistrationForm()
        profile_form = ProfileForm()
    return render(request, 'register.html', {'form': form, 'profile_form': profile_form})



#Profile views
@login_required
def profile(request):
    return render(request, 'profile.html', {'profile': request.user.profile})


@login_required
def profile_update(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {'profile_form': profile_form})



#Admin dashboard views
import matplotlib.pyplot as plt
import io
import urllib, base64
from django.shortcuts import render
from .models import Contact, TeamMember, Discover, MathematicsDocument, PhysicsDocument, ComputerDocument, User


def admin_dashboard(request):
    contact_count = Contact.objects.count()
    team_member_count = TeamMember.objects.count()
    discover_count = Discover.objects.count()
    document_count = MathematicsDocument.objects.count() + PhysicsDocument.objects.count() + ComputerDocument.objects.count()
    user_count = User.objects.count()

    # Assuming admin is the first TeamMember
    admin = TeamMember.objects.first()
    admin_name = admin.name
    admin_role = admin.role
    admin_image = admin.image.url

    # Generate the graph
    counts = [contact_count, team_member_count, document_count, discover_count, user_count]
    labels = ['Contacts', 'Team Members', 'Documents', 'Discover', 'Users']

    fig, ax = plt.subplots()
    ax.plot(labels, [contact_count] * len(labels), label='Contacts', marker='o', color='blue')
    ax.plot(labels, [team_member_count] * len(labels), label='Team Members', marker='o', color='green')
    ax.plot(labels, [document_count] * len(labels), label='Documents', marker='o', color='red')
    ax.plot(labels, [discover_count] * len(labels), label='Discover', marker='o', color='purple')
    ax.plot(labels, [user_count] * len(labels), label='Users', marker='o', color='orange')

    ax.set_xlabel('Categories')
    ax.set_ylabel('Counts')
    ax.set_title('Counts of Each Model')
    ax.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    context = {
        'contact_count': contact_count,
        'team_member_count': team_member_count,
        'discover_count': discover_count,
        'document_count': document_count,
        'user_count': user_count,
        'graph': uri,
        'admin_name': admin_name,
        'admin_role': admin_role,
        'admin_image': admin_image,
    }

    return render(request, 'dashboard.html', context)


#Discover views
def discover_upload(request):
    if request.method == 'POST':
        form = DiscoverUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = DiscoverUploadForm()
    return render(request, 'discover_upload.html', {'form': form})

def discover_list(request):
    discovers = Discover.objects.all()
    return render(request, 'discover_list.html', {'discovers': discovers})

def discover_detail(request, pk):
    discover = get_object_or_404(Discover, pk=pk)
    return render(request, 'discover_detail.html', {'discover': discover})

def edit_discover(request, pk):
    discover = get_object_or_404(Discover, pk=pk)
    if request.method == 'POST':
        form = DiscoverUploadForm(request.POST, request.FILES, instance=discover)
        if form.is_valid():
            form.save()
            return redirect('discover_list')
    else:
        form = DiscoverUploadForm(instance=discover)
    return render(request, 'edit_discover.html', {'form': form})

def delete_discover(request, pk):
    discover = get_object_or_404(Discover, pk=pk)
    if request.method == 'POST':
        discover.delete()
        return redirect('discover_list')
    return render(request, 'delete_discover.html', {'discover': discover})


#Documents views
def document_list(request):
    mathematics_documents = MathematicsDocument.objects.all()
    physics_documents = PhysicsDocument.objects.all()
    computer_documents = ComputerDocument.objects.all()
    return render(request, 'document_list.html', {
        'mathematics_documents': mathematics_documents,
        'physics_documents': physics_documents,
        'computer_documents': computer_documents
    })


def upload_document(request):
    if request.method == 'POST':
        form = UnifiedDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            if subject == 'mathematics':
                MathematicsDocument.objects.create(
                    image=form.cleaned_data['image'],
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    file=form.cleaned_data['file']
                )
            elif subject == 'physics':
                PhysicsDocument.objects.create(
                    image=form.cleaned_data['image'],
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    file=form.cleaned_data['file']
                )
            elif subject == 'computer':
                ComputerDocument.objects.create(
                    image=form.cleaned_data['image'],
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    file=form.cleaned_data['file']
                )
            return redirect('admin_document_list')
    else:
        form = UnifiedDocumentForm()
    return render(request, 'upload_document.html', {'form': form})



def edit_document(request, category, pk):
    if category == 'mathematics':
        document = get_object_or_404(MathematicsDocument, pk=pk)
    elif category == 'physics':
        document = get_object_or_404(PhysicsDocument, pk=pk)
    elif category == 'computer':
        document = get_object_or_404(ComputerDocument, pk=pk)
    else:
        return redirect('admin_document_list')

    if request.method == 'POST':
        form = UnifiedDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document.image = form.cleaned_data['image']
            document.title = form.cleaned_data['title']
            document.description = form.cleaned_data['description']
            document.file = form.cleaned_data['file']
            document.save()
            return redirect('admin_document_list')
    else:
        form = UnifiedDocumentForm(initial={
            'image': document.image,
            'title': document.title,
            'description': document.description,
            'file': document.file,
            'subject': category
        })

    return render(request, 'edit_document.html', {'form': form, 'category': category})


def delete_document(request, category, pk):
    if category == 'mathematics':
        document = get_object_or_404(MathematicsDocument, pk=pk)
    elif category == 'physics':
        document = get_object_or_404(PhysicsDocument, pk=pk)
    elif category == 'computer':
        document = get_object_or_404(ComputerDocument, pk=pk)
    else:
        return redirect('admin_document_list')

    if request.method == 'POST':
        document.delete()
        return redirect('admin_document_list')

    return render(request, 'delete_document.html', {'document': document, 'category': category})

#Users views
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, ProfileForm
from .models import Profile

@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

@login_required
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    profile = get_object_or_404(Profile, user=user)
    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('user_list')
    else:
        user_form = UserChangeForm(instance=user)
        profile_form = ProfileForm(instance=profile)
    return render(request, 'user_edit.html', {'user_form': user_form, 'profile_form': profile_form, 'user': user})

@login_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deregistered successfully.')
        return redirect('user_list')
    return render(request, 'user_delete.html', {'user': user})

@login_required
def user_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'User registered successfully.')
            return redirect('user_list')
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()
    return render(request, 'user_register.html', {'user_form': user_form, 'profile_form': profile_form})


def base(request):
    return render(request, 'base.html')

def admin_landing(request):
    return render(request, 'admin_landing.html')
