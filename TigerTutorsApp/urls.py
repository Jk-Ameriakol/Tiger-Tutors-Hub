
from django.contrib import admin
from django.urls import path

from TigerTutorsApp import views
from django.conf import settings
from django.conf.urls.static import static

from TigerTutorsApp.views import subject_documents, view_pdf, contact_list, \
    edit_contact, delete_contact, edit_team_member, delete_team_member, team_list, register, profile, profile_update

urlpatterns = [
    path('admin/', admin.site.urls),
    path('starter/', views.starter, name='starter'),
    path('', views.landing, name='landing'),
    path('index/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('membership/', views.membership, name='membership'),
    path('team/', views.team, name='team'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('discover_upload/', views.discover_upload, name='discover_upload'),
    path('team_upload/', views.team_upload, name='team_upload'),
    path('upload/', views.upload_document, name='upload_document'),
    path('documents/', views.subject_documents, name='subject_documents'),
    path('documents/<str:subject>/', subject_documents, name='subject_documents'),
    path('documents/<str:subject>/<int:document_id>/', view_pdf, name='view_pdf'),
    path('more/', views.about_more, name='more'),
    path('terms/', views.terms, name='terms'),
    path('pay/', views.pay, name='pay'),
    path('stk/', views.stk, name='stk'),
    path('token/', views.token, name='token'),
    path('contacts/', contact_list, name='contact_list'),
    path('contacts/edit/<int:pk>/', edit_contact, name='edit_contact'),
    path('contacts/delete/<int:pk>/', delete_contact, name='delete_contact'),
    path('team_list/', team_list, name='team_list'),
    path('team/edit/<int:pk>/', edit_team_member, name='edit_team_member'),
    path('team/delete/<int:pk>/', delete_team_member, name='delete_team_member'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('profile/update/', profile_update, name='profile_update'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('discover/', views.discover_list, name='discover_list'),
    path('discover/<int:pk>/', views.discover_detail, name='discover_detail'),
    path('discover/edit/<int:pk>/', views.edit_discover, name='edit_discover'),
    path('discover/delete/<int:pk>/', views.delete_discover, name='delete_discover'),
    path('admindocuments/', views.document_list, name='admin_document_list'),
    path('admindocuments/edit/<str:category>/<int:pk>/', views.edit_document, name='edit_document'),
    path('admindocuments/delete/<str:category>/<int:pk>/', views.delete_document, name='delete_document'),
    path('adminusers/', views.user_list, name='user_list'),
    path('adminusers/edit/<int:pk>/', views.user_edit, name='user_edit'),
    path('adminusers/delete/<int:pk>/', views.user_delete, name='user_delete'),
    path('adminusers/register/', views.user_register, name='user_register'),
    path('base/', views.base, name='base'),
















] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

