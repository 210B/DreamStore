# Generated by Django 4.0.4 on 2022-12-19 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dream', '0009_alter_distributor_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='distributor',
            name='slug',
            field=models.SlugField(allow_unicode=True, max_length=200, null=True, unique=True),
        ),
    ]
