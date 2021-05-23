# Generated by Django 3.1.7 on 2021-04-23 09:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_uservideoset_joined'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmileDos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user1', models.CharField(max_length=100)),
                ('user2', models.CharField(max_length=100)),
                ('smile_dos', models.DecimalField(decimal_places=1, max_digits=4)),
                ('joined', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='SmileRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('video', models.CharField(max_length=100)),
                ('smile_rate', models.DecimalField(decimal_places=1, max_digits=3)),
                ('joined', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.DeleteModel(
            name='UserVideoSet',
        ),
    ]
