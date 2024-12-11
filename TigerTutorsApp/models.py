from django.db import models


# Create your models here.
class Discover(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=500)

    def __str__(self):
        return self.name

from django.db import models
from django.contrib.auth.models import AbstractUser

class Member(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='members/', blank=True, null=True)

    def __str__(self):
        return self.username



    def __str__(self):
        return self.username


    groups = models.ManyToManyField(
        'auth.Group',
        related_name='member_set',  # Custom related name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='member_permission_set',  # Custom related name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username




class Admin(models.Model):
    name = models.CharField(max_length=50)
    username =models.CharField(
        max_length=50,
        unique=True,
    )
    password =models.CharField(
        max_length=8
        ,unique=True
        ,null=False
        ,blank=False
        ,default=''
        ,editable=False
        ,error_messages={'unique':'Username already exists','wrong':'Wrong password'}
        ,help_text='Required. 8 characters or fewer. Letters, digits and @/./+/-/_ only.'
    )

    def __str__(self):
        return self.username

#Subjects Models
class MathematicsDocument(models.Model):
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=50)
    description = models.TextField(200)
    file = models.FileField(upload_to='mathematics/')

    def __str__(self):
        return self.title


class PhysicsDocument(models.Model):
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=50)
    description = models.TextField(200)
    file = models.FileField(upload_to='physics/')

    def __str__(self):
        return self.title


class ComputerDocument(models.Model):
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=50)
    description = models.TextField(200)
    file = models.FileField(upload_to='computer/')

    def __str__(self):
        return self.title

#model code for uploading document for analyzing and then generate questions
class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team/', blank=True, null=True)
    twitter = models.URLField(max_length=200, blank=True, null=True)  # 'X' formerly known as 'Twitter'
    facebook = models.URLField(max_length=200, blank=True, null=True)
    instagram = models.URLField(max_length=200, blank=True, null=True)
    linkedin = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name




