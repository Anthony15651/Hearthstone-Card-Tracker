# Live Project 1

<h1>Introduction:</h1>
<p>This page functions as a summary of the first live project I completed through The Tech Academy. The goal of this project was to provide me with real-world technical experience, and for me to show off some of the skills I've learned so far. During this project, I worked with a team to create apps using the Django framework (version 2.2) that will help users keep track of various collectible items. For my app, I chose to develop a program capable of keeping track of a collection of cards for a popular trading card game, Hearthstone. This project included three main parts, which I will provide details on below.</p>

<h1>CRUD Operations:</h1>
<p>To start the project, I needed to set up CRUD operations to have a basic working product. The CRUD Operations were pretty straightforward, but I ran into two challenges when trying to add aditional features. First, I wanted to Paginate the queried results so that the user could look through multiple pages of cards, rather than one long list. Being new to Pagination and the Django framework in general, it took some practice to understand the idea of passing content from the Views to my templates. I was able to overcome this by referring to the documentation and furthering my comprehension, which brings me to my second challenge. Instead of bringing users to a separate page to confirm deletion of a card in the database, I felt a pop-up modal would be better for the user experience. Using a modal required me to figure out a way to differentiate between either form ("edit_form" or "delete_form"), and act accordingly. I was able to accomplish this simply by adding two "if" statements which check to see which form is sent.</p>

<h4>Views:</h4>

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

<h1>Beautiful Soup:</h1>
<p>After setting up the CRUD Operations, I wanted to use Beautiful Soup to scrape relevant data from the web and display that data </p>

<h1>API:</h1>
<p></p>

<h1>Key Takeaways:</h1>
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
