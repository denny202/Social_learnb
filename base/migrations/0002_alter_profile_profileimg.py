# Generated by Django 4.2.3 on 2023-07-30 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profileimg',
            field=models.ImageField(default='default_user.jpg', upload_to='profile_images/'),
        ),
    ]
