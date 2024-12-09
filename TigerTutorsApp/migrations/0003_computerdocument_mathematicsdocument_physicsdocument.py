# Generated by Django 5.1.3 on 2024-11-30 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TigerTutorsApp', '0002_admin_contact_member'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComputerDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(verbose_name=200)),
                ('file', models.FileField(upload_to='computer/')),
            ],
        ),
        migrations.CreateModel(
            name='MathematicsDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(verbose_name=200)),
                ('file', models.FileField(upload_to='mathematics/')),
            ],
        ),
        migrations.CreateModel(
            name='PhysicsDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(verbose_name=200)),
                ('file', models.FileField(upload_to='physics/')),
            ],
        ),
    ]
