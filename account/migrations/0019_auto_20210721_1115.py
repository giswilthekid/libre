# Generated by Django 3.1.7 on 2021-07-21 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0018_auto_20210719_1059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectlist',
            name='id',
        ),
        migrations.RemoveField(
            model_name='servicelist',
            name='id',
        ),
        migrations.AddField(
            model_name='projectlist',
            name='pl_id',
            field=models.IntegerField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='servicelist',
            name='sl_id',
            field=models.IntegerField(default=2, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
