# Generated by Django 3.1.7 on 2021-07-19 03:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_auto_20210719_0948'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicelist',
            name='basic_packet',
        ),
        migrations.RemoveField(
            model_name='servicelist',
            name='premium_packet',
        ),
        migrations.RemoveField(
            model_name='servicelist',
            name='standard_packet',
        ),
    ]