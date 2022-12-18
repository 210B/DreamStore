# Generated by Django 4.0.4 on 2022-12-18 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dream', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(allow_unicode=True, max_length=200, unique=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='theme',
            options={'verbose_name_plural': 'Themes'},
        ),
    ]
