# Generated by Django 5.1.5 on 2025-02-12 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogviews'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogviews',
            options={'verbose_name': 'Просмотры блога', 'verbose_name_plural': 'Просмотры блога'},
        ),
    ]
