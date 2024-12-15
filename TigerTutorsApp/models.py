from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, Group, Permission



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


#Member model
class Member(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='member_groups',  # Ensure this is unique
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='member_permissions',  # Ensure this is unique
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )



#Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images', blank=True, default='default.jpg')
    email = models.EmailField(max_length=100, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username







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


#Team members model
class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team/', blank=True, null=True)
    twitter = models.URLField(max_length=200, blank=True, null=True)
    facebook = models.URLField(max_length=200, blank=True, null=True)
    instagram = models.URLField(max_length=200, blank=True, null=True)
    linkedin = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name




