# Generated by Django 3.0.6 on 2020-06-10 13:11

from django.db import migrations, models
import multi_email_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('myclass', '0004_auto_20200609_1502'),
    ]

    operations = [
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to', multi_email_field.fields.MultiEmailField()),
                ('expiry_date', models.DateField()),
                ('expiry_time', models.TimeField()),
            ],
        ),
    ]
