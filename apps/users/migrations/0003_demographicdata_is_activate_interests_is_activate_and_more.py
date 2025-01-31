# Generated by Django 5.1.5 on 2025-01-31 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_interests_managers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='demographicdata',
            name='is_activate',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Активируется'),
        ),
        migrations.AddField(
            model_name='interests',
            name='is_activate',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Активируется'),
        ),
        migrations.AddField(
            model_name='medicalhistory',
            name='is_activate',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Активируется'),
        ),
        migrations.AddField(
            model_name='notes',
            name='is_activate',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Активируется'),
        ),
    ]
