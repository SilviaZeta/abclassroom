# Generated by Django 3.0.6 on 2020-06-11 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myclass', '0009_auto_20200610_1633'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_size', models.IntegerField(null=True)),
                ('mylist', models.TextField(blank=True, null=True)),
                ('myclass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class_group', to='myclass.Class')),
            ],
        ),
    ]