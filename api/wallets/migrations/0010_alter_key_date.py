# Generated by Django 3.2.13 on 2022-04-23 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0009_alter_key_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='key',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
