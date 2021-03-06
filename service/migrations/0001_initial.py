# Generated by Django 3.1.7 on 2021-07-12 22:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import service.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceSubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_subname', models.CharField(max_length=100)),
                ('service_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.servicecategory')),
            ],
        ),
        migrations.CreateModel(
            name='ServicePost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('body', models.TextField(max_length=2000)),
                ('image', models.ImageField(blank=True, null=True, upload_to=service.models.upload_location)),
                ('date_published', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('deadline', models.PositiveIntegerField()),
                ('budget', models.BigIntegerField()),
                ('slug', models.SlugField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('service_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.servicecategory')),
                ('service_subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.servicesubcategory')),
            ],
        ),
    ]
