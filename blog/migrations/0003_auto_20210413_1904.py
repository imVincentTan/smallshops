# Generated by Django 3.1.7 on 2021-04-13 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20210413_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='contact_email',
            field=models.EmailField(max_length=254),
        ),
    ]