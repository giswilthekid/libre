# Generated by Django 3.1.7 on 2021-07-17 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_auto_20210717_1833'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basicpacket',
            old_name='basic_packet_service',
            new_name='packet_service',
        ),
        migrations.RenameField(
            model_name='premiumpacket',
            old_name='premium_packet_service',
            new_name='packet_service',
        ),
        migrations.RenameField(
            model_name='standardpacket',
            old_name='standard_packet_service',
            new_name='packet_service',
        ),
    ]
