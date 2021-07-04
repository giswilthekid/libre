# Generated by Django 3.1.7 on 2021-07-03 23:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_auto_20210704_0629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='budget',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.category'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='deadline',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.subcategory'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
