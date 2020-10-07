# Generated by Django 3.1.1 on 2020-09-25 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20200925_0335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='body_part',
            field=models.IntegerField(choices=[(1, 'CHEST'), (2, 'BICEP'), (3, 'CALFS'), (4, 'HASTRINGS'), (5, 'QUADRICEPS'), (6, 'TRICEPS')]),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='difficulty',
            field=models.IntegerField(choices=[(1, 'EASY'), (2, 'NORMAL'), (3, 'HARD'), (4, 'PRO')]),
        ),
    ]