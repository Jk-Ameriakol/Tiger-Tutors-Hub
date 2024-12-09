
from django.contrib import admin
from django.urls import path

from TigerTutorsApp import views
from django.conf import settings
from django.conf.urls.static import static

from TigerTutorsApp.views import subject_documents, view_pdf

urlpatterns = [
    path('admin/', admin.site.urls),
    path('starter/', views.starter, name='starter'),
    path('', views.landing, name='landing'),
    path('index/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('service_details/', views.service_details, name='service_details'),
    path('membership/', views.membership, name='membership'),
    path('team/', views.team, name='team'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('discover_upload/', views.discover_upload, name='discover_upload'),
    path('team_upload/', views.team_upload, name='team_upload'),
    path('upload/', views.upload_document, name='upload_document'),
    path('documents/', views.subject_documents, name='subject_documents'),


    path('documents/<str:subject>/', subject_documents, name='subject_documents'),
    path('documents/<str:subject>/<int:document_id>/', view_pdf, name='view_pdf'),

    path('upload_documents/', views.upload_documents, name='upload_documents'),

    path('more/', views.about_more, name='more'),





] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

