# Generated by Django 3.0.6 on 2020-06-02 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myclass', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='class',
            options={'permissions': (('can_delete_class', 'can delete a class instance'), ('can_update_class', 'can update a class instance'))},
        ),
    ]
