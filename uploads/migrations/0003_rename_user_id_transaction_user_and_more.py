# Generated by Django 4.2.11 on 2024-04-18 22:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0002_transaction_user_id_uploadedfile_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='uploadedfile',
            old_name='user_id',
            new_name='user',
        ),
    ]
