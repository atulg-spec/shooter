# Generated by Django 4.2.7 on 2024-10-13 23:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_remove_messages_content_type_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='messages_sent',
        ),
    ]
