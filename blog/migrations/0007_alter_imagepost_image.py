# Generated by Django 3.2.18 on 2023-03-28 13:40

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20230328_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagepost',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]