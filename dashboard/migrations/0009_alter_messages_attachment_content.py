# Generated by Django 4.2.7 on 2024-11-17 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_messages_attachment_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='attachment_content',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
