# Generated by Django 4.2.7 on 2024-11-15 10:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0004_campaign_frequency'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(default='', max_length=50)),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Custom tag',
                'verbose_name_plural': 'Custom tags',
            },
        ),
        migrations.CreateModel(
            name='tags_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(default='', max_length=500)),
                ('tag', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='dashboard.tags')),
            ],
            options={
                'verbose_name': 'Custom tag data',
                'verbose_name_plural': 'Custom tags Data',
            },
        ),
    ]
