# Generated by Django 3.1.6 on 2021-04-27 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drinx', '0015_auto_20210427_1214'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='content_qty_uni',
            new_name='content_qty_unit',
        ),
    ]