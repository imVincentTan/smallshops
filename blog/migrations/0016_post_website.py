# Generated by Django 3.1.7 on 2021-04-20 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_auto_20210420_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='website',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
