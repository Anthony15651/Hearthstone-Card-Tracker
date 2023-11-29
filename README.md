# Hearthstone Card Tracker
<ul>
    <li><a href="#Introduction">Introduction</a></li>
    <li><a href="#CRUD Operations">CRUD Operations</a></li>
    <li><a href="#Beautiful Soup">Beautiful Soup</a></li>
    <li><a href="#API">API</a></li>
    <li><a href="#Key Takeaways">Key Takeaways</a></li>
</ul>

<h1 id="Introduction">Introduction</h1>
<p>This page functions as a summary of the first live project I completed through The Tech Academy. The goal of this project was to provide me with real-world technical experience, and for me to show off some of the skills I've learned so far. During this project, I worked with a team to create apps using the Django framework (version 2.2) that will help users keep track of various collectible items. We worked together using Azure DevOps. For my app, I chose to develop a program capable of keeping track of a collection of cards for a popular trading card game, Hearthstone. This project included three main parts, which I will provide details on below.</p>

<h1 id="CRUD Operations">CRUD Operations</h1>
<p>To start the project, I needed to set up CRUD operations to have a basic working product. The CRUD Operations were pretty straightforward, but I ran into two challenges when trying to add aditional features. First, I wanted to Paginate the queried results so that the user could look through multiple pages of cards, rather than one long list. Being new to Pagination and the Django framework in general, it took some practice to understand the idea of passing content from the Views to my templates. I was able to overcome this by referring to the documentation and furthering my comprehension, which brings me to my second challenge. Instead of bringing users to a separate page to confirm deletion of a card in the database, I felt a pop-up modal would be better for the user experience. Using a modal required me to figure out a way to differentiate between either form ("edit_form" or "delete_form"), and act accordingly. I was able to accomplish this simply by adding two "if" statements which check to see which form is sent.</p>

<h4>CRUD Views:</h4>

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
        
<h4>Edit / Delete Template:</h4>

    {% extends "HSDT_base.html" %}

    {% block title %}Edit Collection{% endblock %}
    
    {% block content %}
    <h1>Edit Card Info</h1>
    <form method="POST">
        {{ edit_form.as_p }}
        {% csrf_token %}
        <button type="submit" class="btn btn-small">Save</button>
    </form>
    <a href="{% url 'HSDT_details' card.id %}"><button class="btn btn-small">Back</button></a>
    <button class="btn-small btn-delete" id="deleteBtn">Delete</button>
    
    {# This is the modal that pops up to confirm deletion #}
    <div id="deleteModal" class="modal">
        <div class="modal-content">
            <span class="close">&times;</span>
            <h3>Confirm Delete</h3>
            <p>
                Are you sure you would like to delete <span class="bold">{{card.card_name}}</span> ?
                This action cannot be undone.
            </p>
            <form method="POST">
                {{ delete_form }}
                {% csrf_token %}
                <button type="submit" class="btn-delete">Yes, Delete</button>
            </form>
            <p></p>
        </div>
    </div>
    
    {% endblock %}

<h1 id="Beautiful Soup">Beautiful Soup</h1>
<p>After setting up the CRUD Operations, I wanted to use Beautiful Soup to scrape relevant data from the web and display that data to the user. Overall, I feel that the code I've written can be definitely be improved upon, but I'm happy with the results considering this is my first experience with BS. I had my fair share of challenges learning this, but for the sake of keeping this short, I will only include my top two. My first challenge was learning how to scrape the data I need, and then regulating that data so that it all works together. Not every card had all fields entered on the website I was scraping, meaning some returning a value of "None", which would lead to errors when trying to render the page. I was able to figure out the problem by printing the results into my console, and adding an "if" statement to check for such issues. The second challenge was making sure I scraped all the data, and did not include duplicate cards. Because the website I used has multiple pages of cards to go through, I decided to create a list of the URLs, and run BS on each page. To get over the duplicate cards, I added them to a set() and then would check to see if a card is already in the set before adding it. I also Paginated the results so that the user isn't just given one long list, and added dynamic URLs so that clicking on a card name will bring you to that specific card's page.</p>

<h4>Beautiful Soup Views:</h4>

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
                card_name = row.a.string # Gets the string value of the first "a" tag (which happens to be the card name)
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

<h4>Beautiful Soup Template:</h4>

    {% extends "HSDT_base.html" %}
    
    {% block title %}Current Cards{% endblock %}
    
    {# This will be the template to display BS content #}
    {% block content %}
    <h1>Current Standard Cards:</h1>
    <h4>(Data scraped from hearthpwn.com)</h4>
    
    {# Info from BS will be displayed below: #}
    <table>
        <tr>
            <th>Card Name</th>
            <th>Card Type</th>
            <th>Card Class</th>
            <th>Card Rarity</th>
        </tr>
    
    {% for card in page_obj %}
        <tr>
            <td><a href="https://www.hearthpwn.com{{ card.card_url }}" target="_blank">{{ card.card_name }}</a></td>
            <td>{{ card.card_type }}</td>
            <td>{{ card.card_class }}</td>
            <td>{{ card.card_rarity }}</td>
        </tr>
    {% endfor %}
    </table>
    
    {# Below is the code used to display the current page, and the options to go the next/previous page. #}
    <div class="pagination">
        <span class="step-links">
            {% if page_obj.has_previous %}
                <a href="?page=1">&laquo;First</a> |
                <a href="?page={{ page_obj.previous_page_number }}">Previous</a>
            {% endif %}
    
            <span class="current">
                Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}
            </span>
    
            {% if page_obj.has_next %}
                <a href="?page={{ page_obj.next_page_number }}">Next</a> |
                <a href="?page={{ page_obj.paginator.num_pages }}">Last&raquo;</a>
            {% endif %}
        </span>
    </div>
    
    {% endblock %}

![](https://github.com/Anthony15651/Hearthstone-Card-Tracker/blob/main/GIFs/HearthstoneBSGif.mp4)

<h1 id="API">API</h1>
<p>As a bit of a challenge, I wanted to incorporate an API into my project since I had not used one before. Being new to APIs, I decided to use one from RapidAPI as I've heard they are beginner friendly. The API itself offered many different functions, but I was most interested in the search function specifically, which pulls up all cards containing a string searched by the user. I set this up by providing the user with a search box, appending the user's search to my original URL (which is how the search takes place), and then displaying all results. After completing the basic search functionality, I added some code to let users know if their search yeilded no results (the table displays "No Results For [User Search]).</p>

<h4>API Views:</h4>

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
        if search_value is '': # This keeps an error from happening when user first clicks on "API" link
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

<h4>API Template:</h4>

    {% extends "HSDT_base.html" %}

    {% block title %}Search Cards{% endblock %}
    
    {# The goal here is to allow users to search for a string, and then the API will pull
    up all cards which contain the string that the user searched. #}
    
    {% block content %}
    <h1>Card Library Search</h1>
    <h3>Search any string below to see relevant cards:</h3>
    <form method="POST" class="form-text">
        {% csrf_token %}
        {{ search_form.as_p }}
        <button type="submit" class="btn">Search</button>
    </form>
    <br>
    <table>
        <tr>
            <th>Card Name</th>
            <th>Card Type</th>
            <th>Card Class</th>
            <th>Card Rarity</th>
        </tr>
    
    {% for card in card_search %}
        <tr>
            <td>{{ card.name }}</td>
            <td>{{ card.type }}</td>
            <td>{{ card.playerClass }}</td>
            <td>{{ card.rarity }}</td>
        </tr>
    {% endfor %}
    </table>
    {% endblock %}
        
<h1 id="Key Takeaways">Key Takeaways</h1>
<ul>
    <li>
        <b>Planning ahead is an essential part of time management.</b> Taking the time to create a basic outline of what I'm trying to accomplish <i>before</i> starting any coding helps save time in the long run. A few times throughout this project, a idea would pop into my head and I would start coding away, feuled by the excitement of my new goal. I'd spend an hour or two researching, only to realize that implementing my idea would require me to re-write large portions of code. Had I planned ahead more, I would have been able to write my original code more effectively, and saved some time.
    </li>
    <li>
        <b>Always check the documentation first.</b> This project was my first time using things like an API, Beautiful Soup, Pagination, etc., which means I spent a good amount of my time reading up on how to use them. While a quick google search can answer most simple questions, my experience is that the documentation is best when I am completely new to something. I would spend time trying to google parts that I didn't understand, but my google searches weren't always effective because I wouldn't even know the correct terms/keywords to search. Even just skimming through the documentation would tend to point me to my solution faster than most google searches.
    </li>
    <li>
        <b>Take advantage of the console.</b> During the first few days I worked on this project, I spent way too much time trying to find where my errors were. When something didn't work, I would slowly go over all my code, change one line, see if it worked, repeat. Sometimes I would just stare at my code, having no idea why there was an error at all. I began using functions like print(), type(), debug.log(), and console.log() throughout my code to find errors, and it was a night and day difference. While it still took time to work out some of the errors I ran into, using those functions significantly reduced the amount of time it would take for me to identify the cause. 
    </li>
</ul>
