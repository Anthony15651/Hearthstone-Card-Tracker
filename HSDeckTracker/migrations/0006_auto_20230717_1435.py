# Generated by Django 2.2.5 on 2023-07-17 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HSDeckTracker', '0005_auto_20230717_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='card_type',
            field=models.CharField(choices=[('Minion', 'Minion'), ('Ability', 'Ability'), ('Weapon', 'Weapon'), ('Playable Hero', 'Playable Hero'), ('Location', 'Location')], max_length=15),
        ),
    ]
