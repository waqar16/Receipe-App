# Generated by Django 4.2.7 on 2023-12-19 19:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('receip', '0003_receipe_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='receipe',
            old_name='receipe_decription',
            new_name='receipe_description',
        ),
    ]