# Generated by Django 3.2.13 on 2022-04-22 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0003_page_pagetranslation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pubkey',
            old_name='xpub1',
            new_name='xpublic_key',
        ),
        migrations.AddField(
            model_name='key',
            name='xprivate_key',
            field=models.CharField(default=1, max_length=111),
            preserve_default=False,
        ),
    ]