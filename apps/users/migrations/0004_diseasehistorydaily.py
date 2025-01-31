# Generated by Django 5.1.5 on 2025-01-31 13:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_demographicdata_is_activate_interests_is_activate_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DiseaseHistoryDaily',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, null=True, verbose_name='Ежедневное написание статей о болезнях')),
                ('is_activate', models.BooleanField(blank=True, default=False, null=True, verbose_name='Активируется')),
                ('created_at', models.DateField(auto_now_add=True, null=True, verbose_name='Дата публикации')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_disease_history_daily', to=settings.AUTH_USER_MODEL, verbose_name='Интерес пользователя')),
            ],
            options={
                'verbose_name': 'История пользователя ежедневно',
                'verbose_name_plural': 'История пользователя ежедневно',
            },
        ),
    ]
