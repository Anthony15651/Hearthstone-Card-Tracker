# Generated by Django 2.2.5 on 2023-07-11 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HSDeckTracker', '0002_auto_20230711_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='card_class',
            field=models.CharField(choices=[('Death Knight', 'Death Knight'), ('Demon Hunter', 'Demon Hunter'), ('Druid', 'Druid'), ('Hunter', 'Hunter'), ('Mage', 'Mage'), ('Paladin', 'Paladin'), ('Priest', 'Priest'), ('Rogue', 'Rogue'), ('Shaman', 'Shaman'), ('Warlock', 'Warlock'), ('Warrior', 'Warrior'), ('Neutral', 'Neutral')], max_length=20),
        ),
        migrations.AlterField(
            model_name='card',
            name='card_rarity',
            field=models.CharField(choices=[('Common', 'Common'), ('Rare', 'Rare'), ('Epic', 'Epic'), ('Legendary', 'Legendary')], max_length=10),
        ),
        migrations.AlterField(
            model_name='card',
            name='card_type',
            field=models.CharField(choices=[('Minion', 'Minion'), ('Spell', 'Spell'), ('Weapon', 'Weapon'), ('Hero', 'Hero'), ('Location', 'Location')], max_length=10),
        ),
    ]
