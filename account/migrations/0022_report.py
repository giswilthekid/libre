# Generated by Django 3.1.7 on 2021-07-27 12:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0008_auto_20210719_1056'),
        ('blog', '0017_auto_20210725_2058'),
        ('account', '0021_projectlist_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('report_id', models.IntegerField(primary_key=True, serialize=False)),
                ('report_text', models.CharField(blank=True, max_length=2000, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='timestamp')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.blogpost')),
                ('report_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='service.servicepost')),
            ],
        ),
    ]
