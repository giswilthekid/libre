# Generated by Django 3.1.7 on 2021-06-28 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20210628_1632'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='slug',
            new_name='slug_acc',
        ),
    ]
