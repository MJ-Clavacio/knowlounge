# Generated by Django 4.2 on 2023-05-12 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_room_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='link',
            field=models.TextField(blank=True, null=True),
        ),
    ]