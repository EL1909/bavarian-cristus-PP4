# Generated by Django 3.2.18 on 2023-03-24 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20230323_1139'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imagepost',
            old_name='content',
            new_name='text',
        ),
    ]