# Generated by Django 3.2.13 on 2022-04-23 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0005_remove_key_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='key',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]
