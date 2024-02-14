from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse , Http404
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf ,analyze_review_sentiments,post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request,'djangoapp/about.html')
# ...


# Create a `contact` view to return a static contact page
def contact(request):
    company_info = settings.COMPANY_INFO   
    return render(request,'djangoapp/contact_us.html',{'company_info': company_info})

# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            request.session.pop('login_error', None)
            user = form.get_user()
            login(request, user)
            # Redirect to the home page or any other desired page upon successful login
            return redirect('djangoapp:index')
        else:
            # todo put the wrong data to index.html 
            print('wrong pass or username')
            request.session['login_data'] = request.POST
            request.session['login_error'] = '<strong>Not authorized!</strong> Your pass or username is wrong !'
            return redirect('djangoapp:index')
    else:
        print('there is no separate page for login! you can have it in index.html')
        raise Http404("Page not found")
# ...

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)    
    return redirect('djangoapp:index')
# ...

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('djangoapp:index')
        else:                     
            context = {'inputs': request.POST , 'formError':form.errors}
            return render(request,'djangoapp/registration.html',context)
        
    if request.method == 'GET':
        return render(request,'djangoapp/registration.html')
# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":      
        url = f"{settings.DATABASE_URLS['dealerships']}/dealerships/get"         
        # Get dealers from the URL        
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == 'GET':               
        url = f"{settings.DATABASE_URLS['reviews']}/api/get_reviews"  
        reviews = get_dealer_reviews_from_cf(url,dealer_id)
        for review in reviews:
            review.sentiment = analyze_review_sentiments(review.review)                          
        return HttpResponse(reviews)

# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == "POST":
        url = f"{settings.DATABASE_URLS['reviews']}/api/post_review" 
        print(url)
        if not request.user.is_authenticated:
            return HttpResponse("Unauthorized", status=401)
        review = {
            "id": request.POST.get("id"),
            "name": request.POST.get("name"),
            "dealership": int(dealer_id),
            "review": request.POST.get("review"),
            "purchase": request.POST.get("purchase"),
            "purchase_date": request.POST.get("purchase_date"),
            "car_make": request.POST.get("car_make"),
            "car_model": request.POST.get("car_model"),
            "car_year": request.POST.get("car_year")
        }        
        # print('*************************************===')
        # print(json_payload)
        # return HttpResponse(json_payload)
        response = post_request(url, review)
        if response:
            # Optionally, you can return the response content or status code                    
            return HttpResponse(response['message'], 201)

        else:
            return HttpResponse("Failed to post review", status=500)
    else:
        return HttpResponse("Method not allowed", status=405)
# ...


def home(request):  
    return render(request, 'djangoapp/index.html')