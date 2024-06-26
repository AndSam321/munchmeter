# Generated by Django 5.0.6 on 2024-05-18 01:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counter', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='created',
        ),
        migrations.RemoveField(
            model_name='food',
            name='description',
        ),
        migrations.RemoveField(
            model_name='food',
            name='updated',
        ),
        migrations.AddField(
            model_name='food',
            name='carbs',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='food',
            name='protein',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='food',
            name='calories',
            field=models.FloatField(),
        ),
        migrations.CreateModel(
            name='FoodEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('meal_type', models.CharField(choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner')], max_length=10)),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='counter.food')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
