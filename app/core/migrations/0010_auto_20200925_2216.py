# Generated by Django 3.1.1 on 2020-09-25 22:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20200925_0430'),
    ]

    operations = [
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='exercise',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='WorkOut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, unique=True)),
                ('sets', models.ManyToManyField(through='core.Set', to='core.Exercise')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.AddField(
            model_name='set',
            name='exercise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.exercise'),
        ),
        migrations.AddField(
            model_name='set',
            name='work_out',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.workout'),
        ),
        migrations.CreateModel(
            name='Serie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reps', models.IntegerField(default=0)),
                ('weight', models.FloatField(default=0.0)),
                ('comment', models.TextField(blank=True)),
                ('set_bellown', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.set')),
            ],
        ),
    ]