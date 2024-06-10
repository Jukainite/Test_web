# Generated by Django 5.0.6 on 2024-05-31 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_finger_image_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='face_image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='face_images')),
            ],
        ),
    ]
