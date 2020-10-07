# Generated by Django 3.1.1 on 2020-10-04 00:06

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20201003_0215'),
    ]

    operations = [
        migrations.CreateModel(
            name='Routine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='serie',
            name='rpe',
            field=models.IntegerField(default=7, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='set',
            name='work_out',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.workout'),
        ),
        migrations.AlterField(
            model_name='workout',
            name='workout_date',
            field=models.DateField(unique=True),
        ),
        migrations.CreateModel(
            name='RoutineDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField(validators=[django.core.validators.MaxValueValidator(7), django.core.validators.MinValueValidator(1)])),
                ('routine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routines', to='core.routine')),
                ('sets', models.ManyToManyField(blank=True, through='core.Set', to='core.Exercise')),
            ],
        ),
        migrations.AddField(
            model_name='set',
            name='routine',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.routineday'),
        ),
    ]
