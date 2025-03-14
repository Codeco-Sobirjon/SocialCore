# Generated by Django 5.1.5 on 2025-02-15 05:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_blogviews_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='blog/images/', verbose_name='')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='blog.blog', verbose_name='Блог')),
            ],
            options={
                'verbose_name': 'Изображения блога',
                'verbose_name_plural': 'Изображения блога',
            },
        ),
    ]
