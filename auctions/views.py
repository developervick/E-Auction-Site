from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from . import models
from . import forms
from django.db.models import Max


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = models.User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


#! ######################### Project views ##############################



#* done
def index(request):

    """
    This view maps to active listing route
    This View handels index page, Return all the listings from databse
    """

    active_listings = models.listing.objects.filter(status= True)
    return render(request, 'auctions/active.html', {"listing": active_listings})


def active(request):

    all_listings = models.listing.objects.all()
    return render(request, "auctions/index.html", {"listing": all_listings, 'title': 'Home'})
    



def categories(request, category):
    """
    Returns list of categories
    """

    if category == 'all':
        
        cat_list = models.listing.objects.all().values_list('category', flat= True ).distinct()
        return render(request, 'auctions/categories.html', { 'categories': cat_list })


    else:
        cat_list = models.listing.objects.filter(category = category)
        count = models.listing.objects.filter(category = category).count()
        return render(request, 'auctions/categories.html', { 'cat_list': cat_list, 'category': category })



@login_required(login_url='/login')
def watchlist(request):

    user = request.session.get('_auth_user_id')
    user = models.User.objects.get(id = user) 
    
    q = models.watch_list.objects.filter(user_id= user)
    

    if request.method == "POST":
        
        if request.POST.get('watchlist') != None:
            try:
                id = request.POST['watchlist']
                id = models.listing.objects.get(pk = id)
                rec = models.watch_list.objects.create(user_id = user, listing_id = id)
                rec.save()
                count = models.watch_list.objects.filter(user_id= user).count() 
                return render(request, 'auctions/watchlist.html', {'watchlist': q, "count": count})
            except:
                count = models.watch_list.objects.filter(user_id= user).count()
                return render(request, 'auctions/watchlist.html', {'watchlist': q, "count": count})

        else:
            id = request.POST['watchlist_del']
            try:
                rec = models.watch_list.objects.get(pk=id).delete()
                

            except:
                rec = models.watch_list.objects.get(user_id = user, listing_id = id).delete()
                
                 
            count = models.watch_list.objects.filter(user_id= user).count() 
            return render(request, "auctions/watchlist.html", {"watchlist": q, "count": count})

    count = models.watch_list.objects.filter(user_id= user).count() 
    return render(request, 'auctions/watchlist.html', {'watchlist': q, "count": count})



#* done
@login_required(login_url='/login')
def create_listing(request):

    if request.method == 'POST': 
        form = forms.listing_form(request.POST, request.FILES)
        
        if form.is_valid():
            form = form.clean()
            
            # user 
            user_id = request.session.get("_auth_user_id")
            user = models.User.objects.get(pk= user_id)


            listing = models.listing.objects.create(
            bid_price = form['bid_price'],
            current_price = form['bid_price'],
            title = form['title'],
            description = form['description'],
            category = form['category'],
            image = form['image'],
            user_id = user
            )

            listing.save()
            messages.success(request, 'Succesfully created entry')
            return redirect('index')
        
        else:
            return render(request, "auctions/create.html", { 'errors': form.errors })        

    else:
        return render(request, 'auctions/create.html', { 'form': forms.listing_form() })




def listinge_page(request, id):

    closing_eligibility = False
    bids_form = forms.bids_form(request.POST)
    closing = forms.close_listing_form(request.POST)
    
    

    listing = models.listing.objects.get(pk=id)

    bids = models.bids.objects.filter(listing_id= listing).order_by('-id')[:10]


    
    #block to handle watchlist button
    in_watchlist = False

    closing_eligibility = False
    try: 

        user_id = request.session.get("_auth_user_id")
        user = models.User.objects.get(pk= user_id)

        your_watchlist = models.watch_list.objects.filter(user_id= user)

        your_listing = models.listing.objects.filter(user_id=user)

        if listing in your_listing:
            closing_eligibility = True


        watchlist_listing = models.watch_list.objects.get(listing_id=listing)
        if watchlist_listing in your_watchlist:
            in_watchlist = True

    except:
        pass


    #handle post Request
    if request.method == 'POST':
        
        #Block to handle comment form

        #block to handle bid form


        #Block to handle status Form
        
        if closing.is_valid():
            status = closing.cleaned_data['status']

            if status == 'F':
                listing.status = False
                listing.save()
            
    won_user = None
    # getting max value
    if listing.status == False:
        try:
            won_user = bids[0].user_id.username

        except:
            pass

    comments = models.comments.objects.filter(listing_id=listing)
    count = comments.count()
    return render(request, "auctions/listing.html", {'q': listing,
             'comments':comments,
              'count':count,
              'bids': bids, 
              'form': bids_form,
              'closing': closing_eligibility,
              'closing_form':closing,
              'in_watchlist': in_watchlist,
              'won_user': won_user})


@login_required(login_url='/login')
def your_listing(request):

    user_id = request.session.get("_auth_user_id")
    user = models.User.objects.get(pk= user_id)

    your_listing = models.listing.objects.filter(user_id= user)

    return render(request, 'auctions/your_listings.html', { 'your_listing': your_listing})



@login_required(login_url='/login') 
def comment(request, id):

    user_id = request.session.get("_auth_user_id")
    user = models.User.objects.get(pk= user_id)

    listing = models.listing.objects.get(pk=id)

    if request.method == 'POST':

        comment = forms.comment_form(request.POST)
        if comment.is_valid():

            comment = models.comments.objects.create(
                listing_id = listing,
                user_id = user,
                comment= comment.cleaned_data['comment']
            )
            comment.save()
            return HttpResponseRedirect(reverse('listing', kwargs={'id': id}))


@login_required(login_url='/login')
def make_bid(request, id):
    
    user_id = request.session.get("_auth_user_id")
    user = models.User.objects.get(pk= user_id)
    bids_form = forms.bids_form(request.POST)
    listing = models.listing.objects.get(pk=id)

    if request.method == "POST":

        if bids_form.is_valid():

            bid = bids_form.cleaned_data['value']
            current_bid = listing.current_price
            
            if current_bid < bid:
                

                new_bid = models.bids.objects.create(user_id=user, listing_id=listing, value=bid)
                new_bid.save()

                listing.current_price = bid
                listing.save()                
                return HttpResponseRedirect(reverse('listing', kwargs={'id': id}))

            else:
                messages.info(request, 'Bid must be greater than Current Bid')
                return HttpResponseRedirect(reverse('listing', kwargs={'id': id}))

