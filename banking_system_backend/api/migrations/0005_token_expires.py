# Generated by Django 4.1 on 2023-05-11 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='expires',
            field=models.DateTimeField(default=None),
        ),
    ]
