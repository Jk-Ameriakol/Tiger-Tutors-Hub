import logging

import openai
import requests
from PyPDF2 import PdfReader
from django.shortcuts import render, redirect, get_object_or_404
from .models import Discover, Contact, Member, MathematicsDocument, PhysicsDocument, ComputerDocument, TeamMember
from .forms import DiscoverUploadForm, UnifiedDocumentForm, DocumentForm, TeamMemberForm
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


def register(request):
    if request.method=='POST':
        members= Member(
            name=request.POST['name'],
            username=request.POST['username'],
            password=request.POST['password'],
        )
        members.save()
        return redirect('/login')
    else:
        return render(request,'register.html')

def login(request):
    return render(request,'login.html')



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

# Set your OpenAI API key
openai.api_key = 'f3ae1f91e64243848863cc86c2f480fb'

def extract_text_from_file(file_path):
    if file_path.endswith('.pdf'):
        reader = PdfReader(file_path)
        text = " ".join([page.extract_text() for page in reader.pages])
    elif file_path.endswith('.docx'):
        doc = DocxDocument(file_path)
        text = " ".join([paragraph.text for paragraph in doc.paragraphs])
    else:
        text = ""
    return text

logging.basicConfig(level=logging.DEBUG)


API_KEY = '79914965d4464e7e9c45dea5840ebd3b'
API_URL = 'https://api.aimlapi.com/v1/chat/completions'


def generate_questions(text):
    """
    Generate questions from the given text using the AIML API.
    """
    system_prompt = "You are a helpful assistant that generates questions from text."
    user_prompt = f"Generate as many questions as possible from the following text:\n\n{text}"

    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 256,
    }

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad responses

        # Extract questions from the response
        data = response.json()
        questions = data.get('choices', [])[0].get('message', {}).get('content', '').strip()
        return questions.split("\n")  # Return a list of questions
    except requests.exceptions.RequestException as e:
        logging.error(f"API Request failed: {e}")
        return [f"Error: {str(e)}"]

def upload_documents(request):
    """
    Handles document uploads and generates questions from the content.
    """
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded document
            document = form.save()
            file_path = document.file.path

            # Extract text from the uploaded file
            text = extract_text_from_file(file_path)

            # Generate questions using the AIML API
            questions = generate_questions(text)

            # Render the questions on the results page
            return render(request, 'results.html', {
                'questions': questions,
                'file_url': document.file.url
            })
    else:
        form = DocumentForm()

    return render(request, 'uploads.html', {'form': form})

# def generate_questions(text):
#     url = 'https://api.aimlapi.com/v1'
#     headers = {'Authorization': f'Bearer {'f3ae1f91e64243848863cc86c2f480fb'}',
#                'Content-Type': 'application/json'}
#     payload = {'text': text}
#
#     response = requests.post(url, headers=headers, json=payload)
#
#     if response.status_code == 200:
#         data = response.json()
#         questions = data.get('questions', [])
#         return "\n".join(questions)
#     else:
#         return "An error occurred while generating questions."


# def upload_documents(request):
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             document = form.save()
#             file_path = document.file.path
#             text = extract_text_from_file(file_path)
#             questions = generate_questions(text)
#
#             return render(request, 'results.html', {
#                 'questions': questions,
#                 'file_url': document.file.url
#             })
#     else:
#         form = DocumentForm()
#
#     return render(request, 'uploads.html', {'form': form})


# def upload_documents(request):
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             document = form.save()
#             file_path = document.file.path
#             text = extract_text_from_file(file_path)
#             questions = generate_questions(text)
#
#             return render(request, 'results.html', {
#                 'questions': questions,
#                 'file_url': document.file.url
#             })
#     else:
#         form = DocumentForm()
#
#     return render(request, 'uploads.html', {'form': form})


def about_more(request):
    return render(request,'about_more.html')

def service_details(request):
    return render(request,'service-details.html')






