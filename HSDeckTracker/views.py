from django.shortcuts import render, redirect, get_object_or_404
from .forms import CardForm, DeleteCardForm, SearchForm
from .models import Card
import requests
from django.core.paginator import Paginator
from bs4 import BeautifulSoup
import re

# Create your views here.

# Function to view "home" page
def HSDT_home(request):
    return render(request, 'HSDeckTracker/HSDT_home.html')

# Function to view "add card" page
def HSDT_create(request):
    form = CardForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('HSDT_read')
    content = {'form': form}
    return render(request, 'HSDeckTracker/HSDT_create.html', content)

# Function to display items using Paginator
def HSDT_read(request):
    card_list = Card.Cards.all()
    paginator = Paginator(card_list, 5)

    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, 'HSDeckTracker/HSDT_read.html', {"page_obj": page_obj})

# Function to view "details" page
def HSDT_details(request, pk):
    card = get_object_or_404(Card, pk=pk)
    content = {'card': card}
    return render(request, 'HSDeckTracker/HSDT_details.html', content)

# Function to edit / delete cards. This function checks the form first to see which it is, then acts accordingly.
def HSDT_edit(request, pk):
    card = get_object_or_404(Card, pk=pk)
    edit_form = CardForm(data=request.POST or None, instance=card)
    delete_form = DeleteCardForm()
    if request.method == "POST":
        if 'edit_form' in request.POST:
            edit_form = CardForm(request.POST, instance=card)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('../../read')
        if 'delete_form' in request.POST:
            delete_form = DeleteCardForm(request.POST)
            if delete_form.is_valid():
                card.delete()
                return redirect('../../read')
    context = {
        'card': card,
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'HSDeckTracker/HSDT_edit.html', context=context)

# Function for Beautiful Soup. This extracts data from hearthpwn.com,
# and then displays that data in a cleaned up format.
def HSDT_bs(request):
    URLS = [
        "https://www.hearthpwn.com/cards?filter-set=1800",
        "https://www.hearthpwn.com/cards?filter-set=1800&page=2",
        "https://www.hearthpwn.com/cards?filter-set=1800&page=3",
        "https://www.hearthpwn.com/cards?filter-set=1800&page=4"
    ]
    cards = []
    card_name_set = set() # Using the set method to remove duplicate names later on
    for URL in URLS: # Goes through all paginated pages on hearthpwn.com/cards?filter-set=1800
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('div', attrs={'class': 'listing-body'}) # Finds specific data we are looking for
        for row in table.findAll('td', attrs={'class': 'visual-details-cell'}): # Runs through this loop for each card
            card_name = row.h3.a.string # Gets the string value of the first "a" tag (which happens to be the card name)
            if card_name in card_name_set: # The website pulled several duplicate names
                continue # I've added this loop to make sure only one of each card is shown.
            else:
                card_name_set.add(card_name)
                card_url = row.a['href']  # Gets the url for each card
                card_type = row.ul.li.a.string # Gets the string value for "type"
                card_rarity_tag = row.find(href=re.compile("filter-rarity")) # Gets the card's rarity tag
                if card_rarity_tag is not None:
                    card_rarity = card_rarity_tag.string
                else:
                    card_rarity = "No Rarity"
                card_class_tag = row.find(href=re.compile("filter-class")) # Gets card class tag
                if card_class_tag is not None:
                    card_class = card_class_tag.get_text()
                else:
                    card_class = "Neutral"
                cards.append({
                    'card_url': card_url,
                    'card_name': card_name,
                    'card_type': card_type,
                    'card_rarity': card_rarity,
                    'card_class': card_class
                }) # Adds card data to the list
    paginator = Paginator(cards, 40) # Paginates the list we get back by 40
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    content = {'page_obj': page_obj}
    return render(request, 'HSDeckTracker/HSDT_bs.html', content)

# Function for my API. This uses the API to search any string, and return all cards that contain
# the string searched by the user.
def HSDT_api(request):
    URL = "https://omgvamp-hearthstone-v1.p.rapidapi.com/cards/search/"
    headers = {
        "X-RapidAPI-Key": "a8d5f261eemsh408d2d3165b6702p168636jsnd42e645665bb",
        "X-RapidAPI-Host": "omgvamp-hearthstone-v1.p.rapidapi.com"
    }
    search_form = SearchForm(data=request.POST or None)
    search_value = '' # This keeps an error from happening when user first clicks on "API" link
    if request.method == 'POST':
        if search_form.is_valid():
            search_value = search_form.cleaned_data # Removes HTML tags from string
            URL += search_value['search_value'] # Adds user's string to the end of the URL
    response = requests.get(URL, headers=headers)
    card_search = response.json()
    if search_value == '': # This keeps an error from happening when user first clicks on "API" link
        card_search = []
    elif card_search == {'error': 404, 'message': 'Card not found.'}: # Lets the user know if there are no results
        card_search = [{
            'name': 'No',
            'type': 'Results',
            'playerClass': 'For',
            'rarity': search_value['search_value']
        }]
    content = {
        'card_search': card_search,
        'search_form': search_form,
    }
    return render(request, 'HSDeckTracker/HSDT_api.html', content)
