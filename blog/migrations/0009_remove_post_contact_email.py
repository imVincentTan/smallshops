# Generated by Django 3.1.7 on 2021-04-14 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_post_contact_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='contact_email',
        ),
    ]
