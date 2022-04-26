# Generated by Django 3.2.13 on 2022-04-24 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0012_auto_20220424_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pubkey',
            name='key',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wallet_public_keys', to='wallets.key'),
        ),
        migrations.AlterField(
            model_name='pubkey',
            name='xpublic_key',
            field=models.CharField(max_length=130),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='keys',
            field=models.ManyToManyField(related_name='public_keys', to='wallets.PubKey'),
        ),
    ]
