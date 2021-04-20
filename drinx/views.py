from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
from .models import User
from django.contrib.admin.views.decorators import staff_member_required
import os

# Create your views here.
def index(request):
    #message = os.environ['TEST_ENV_VAR']
    #return HttpResponse(message)
    #return HttpResponse('Hello World!')

    return render(request, "drinx/index.html")

def login_view(request):
    if request.method == "POST":

            # Attempt to sign user in
            email = request.POST["email"]
            username = User.objects.get(email=email.lower()).username
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "drinx/login.html", {
                    "message": "Invalid email and/or password."
                })
    else:
        return render(request, "drinx/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register_view(request):
    if request.method == "POST":
        username = request.POST["email"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        deliv_address_street = request.POST["street"]
        deliv_address_houseno = request.POST["house_number"]
        deliv_address_zipcode = request.POST["zipcode"]
        deliv_address_city = request.POST["city"]


        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmedpassword = request.POST["confirmedpassword"]
        if password != confirmedpassword:
            return render(request, "drinx/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name,\
                    last_name=last_name, deliv_address_street=deliv_address_street, deliv_address_houseno=deliv_address_houseno,\
                    deliv_address_zipcode=deliv_address_zipcode, deliv_address_city=deliv_address_city)
            user.save()
        except IntegrityError:
            return render(request, "drinx/register.html", {
                "message": "Something went wrong. Probably Email already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "drinx/register.html")

@staff_member_required
def backend_index(request):

    return render(request, "drinx/backend_index.html")

@staff_member_required
def backend_categories(request):

    return render(request, "drinx/backend_categories.html")