# Generated by Django 5.1.5 on 2025-01-31 07:35

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
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True, verbose_name='Время начала')),
                ('initiator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='convo_starter', to=settings.AUTH_USER_MODEL, verbose_name='Инициатор')),
                ('receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='convo_participant', to=settings.AUTH_USER_MODEL, verbose_name='Получатель')),
            ],
            options={
                'verbose_name': '1. Беседа',
                'verbose_name_plural': '1. Беседы',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=200, verbose_name='Текст')),
                ('attachment', models.FileField(blank=True, upload_to='', verbose_name='Вложение')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Время отправки')),
                ('conversation_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.conversation', verbose_name='Идентификатор беседы')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='message_sender', to=settings.AUTH_USER_MODEL, verbose_name='Отправитель')),
            ],
            options={
                'verbose_name': '2. Сообщение',
                'verbose_name_plural': '2. Сообщения',
                'ordering': ('-timestamp',),
            },
        ),
    ]
