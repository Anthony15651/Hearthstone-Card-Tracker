# Live Project 1

<h1>Introduction:</h1>
<p>This page functions as a summary of the first live project I completed through The Tech Academy. The goal of this project was to provide me with real-world technical experience, and for me to show off some of the skills I've learned so far. During this project, I worked with a team to create apps using the Django framework (version 2.2) that will help users keep track of various collectible items. For my app, I chose to develop a program capable of keeping track of a collection of cards for a popular trading card game, Hearthstone. This project included three main parts, which I will provide details on below.</p>

<h1>CRUD Operations:</h1>
<p>To start the project, I needed to set up CRUD operations to have a basic working product. </p>
~~~
# Function to view "home" page
def HSDT_home(request):
    return render(request, 'HSDeckTracker/HSDT_home.html')

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
~~~
