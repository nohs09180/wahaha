# Generated by Django 3.1.7 on 2021-04-22 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_video_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserVideoSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('video', models.CharField(max_length=100)),
            ],
        ),
    ]
