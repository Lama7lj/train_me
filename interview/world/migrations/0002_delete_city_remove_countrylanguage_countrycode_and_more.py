# Generated by Django 5.0.4 on 2024-04-23 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='City',
        ),
        migrations.RemoveField(
            model_name='countrylanguage',
            name='countrycode',
        ),
        migrations.DeleteModel(
            name='Country',
        ),
        migrations.DeleteModel(
            name='Countrylanguage',
        ),
    ]
