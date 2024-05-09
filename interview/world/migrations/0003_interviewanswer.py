# Generated by Django 5.0.4 on 2024-05-01 21:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0002_delete_city_remove_countrylanguage_countrycode_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='InterviewAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about_yourself', models.TextField()),
                ('hear_about', models.TextField()),
                ('company_info', models.TextField()),
                ('apply_position', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
