# Generated by Django 3.1.1 on 2020-10-07 04:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20201007_0253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='routineday',
            name='sets',
        ),
    ]