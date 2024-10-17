# Generated by Django 5.0.3 on 2024-09-17 20:23

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
            name='Messages',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('subject', models.CharField(default='', max_length=150)),
                ('content_type', models.CharField(choices=[('text', 'text'), ('html', 'html')], default='text', max_length=12)),
                ('content', models.TextField()),
                ('massenger', models.CharField(choices=[('Email', 'Email')], default='Email', max_length=15)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
        ),
        migrations.CreateModel(
            name='messages_sent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('interacted_users', models.PositiveIntegerField(default=0)),
                ('platform', models.CharField(choices=[('Email', 'Email')], default='Email', max_length=12)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('message', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.messages')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Message sent',
                'verbose_name_plural': 'Delivered messages',
            },
        ),
    ]