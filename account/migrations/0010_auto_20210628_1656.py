# Generated by Django 3.1.7 on 2021-06-28 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20210628_1650'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='slug_acc',
            new_name='slug',
        ),
    ]
