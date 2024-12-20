# Generated by Django 5.1.3 on 2024-12-13 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TigerTutorsApp', '0013_profile_delete_admin_delete_document_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='default.jpg', upload_to='profile_images'),
        ),
    ]
