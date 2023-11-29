from django.db import models
from django.views.generic import ListView
from django import forms

# Create your models here.

types_choices = [
    ('Minion', 'Minion'),
    ('Ability', 'Ability'),
    ('Weapon', 'Weapon'),
    ('Playable Hero', 'Playable Hero'),
    ('Location', 'Location'),
]

classes_choices = [
    ('Death Knight', 'Death Knight'),
    ('Demon Hunter', 'Demon Hunter'),
    ('Druid', 'Druid'),
    ('Hunter', 'Hunter'),
    ('Mage', 'Mage'),
    ('Paladin', 'Paladin'),
    ('Priest', 'Priest'),
    ('Rogue', 'Rogue'),
    ('Shaman', 'Shaman'),
    ('Warlock', 'Warlock'),
    ('Warrior', 'Warrior'),
    ('Neutral', 'Neutral'),
]

rarity_choices = [
    ('Common', 'Common'),
    ('Rare', 'Rare'),
    ('Epic', 'Epic'),
    ('Legendary', 'Legendary'),
]


class Card(models.Model):
    card_name = models.CharField(max_length=50)
    card_cost = models.IntegerField()
    card_class = models.CharField(max_length=20, choices=classes_choices)
    card_type = models.CharField(max_length=15, choices=types_choices)
    card_rarity = models.CharField(max_length=10, choices=rarity_choices)
    card_image_link = models.CharField(max_length=100)
    card_description = models.TextField(max_length=250)

    Cards = models.Manager()

    def __str__(self):
        return self.card_name



class CardSearch(models.Model):
    search_value = models.CharField(max_length=30)
