# Generated by Django 5.1.1 on 2024-09-15 17:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('free', 'Вільний'), ('busy', 'Зайнятий')], default='free', max_length=10)),
            ],
            options={
                'verbose_name': 'Транспорт',
                'verbose_name_plural': 'Транспортні засоби',
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_time_start', models.DateTimeField()),
                ('booking_time_end', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('transport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking_app.transport')),
            ],
            options={
                'verbose_name': 'Бронювання',
                'verbose_name_plural': 'Бронювання',
            },
        ),
    ]
