# Generated by Django 5.0.6 on 2024-06-04 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_rename_bill_id_qr_image_bill'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qr_image',
            name='id',
        ),
        migrations.AlterField(
            model_name='qr_image',
            name='bill',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
    ]
