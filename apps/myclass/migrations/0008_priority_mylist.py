# Generated by Django 3.0.6 on 2020-06-10 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myclass', '0007_auto_20200610_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='priority',
            name='mylist',
            field=models.TextField(blank=True),
        ),
    ]
