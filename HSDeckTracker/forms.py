from django import forms
from django.forms import ModelForm, TextInput, NumberInput, Select, Textarea
from .models import Card, CardSearch


class CardForm(ModelForm):
    edit_form = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    class Meta:
        model = Card
        fields = ['card_name', 'card_cost', 'card_class', 'card_type', 'card_rarity', 'card_image_link',
                  'card_description']
        labels = {
            'card_name': '',
            'card_cost': '',
            'card_class': '',
            'card_type': '',
            'card_rarity': '',
            'card_image_link': '',
            'card_description': '',
        }
        widgets = {
            'card_name': TextInput(attrs={
                'class': 'text-form',
                'placeholder': 'Card Name',
            }),
            'card_cost': NumberInput(attrs={
                'class': 'text-form',
                'placeholder': 'Card Cost',
            }),
            'card_class': Select(attrs={
                'class': 'text-form',
                'placeholder': 'Card Class',
            }),
            'card_type': Select(attrs={
                'class': 'text-form',
                'placeholder': 'Card Type',
            }),
            'card_rarity': Select(attrs={
                'class': 'text-form',
                'placeholder': 'Card Rarity',
            }),
            'card_image_link': TextInput(attrs={
                'class': 'text-form',
                'placeholder': 'Card Image Link',
            }),
            'card_description': Textarea(attrs={
                'class': 'text-form-big',
                'placeholder': 'Card Description',
            }),
        }

class DeleteCardForm(ModelForm):
    delete_form = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    class Meta:
        model = Card
        fields = []

class SearchForm(ModelForm):
    class Meta:
        model = CardSearch
        fields = ['search_value']
        labels = {
            'search_value': '',
        }
        widgets = {
            'search_value': TextInput(attrs={
                'class': 'text-form',
                'placeholder': 'Type any value to search...',
            })
        }



