# Generated by Django 3.0.6 on 2020-05-29 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.PositiveSmallIntegerField(choices=[(1, 'student'), (2, 'supervisor'), (3, 'admin')], primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='roles',
            field=models.ManyToManyField(to='account.Role'),
        ),
    ]
