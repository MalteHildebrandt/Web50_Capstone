from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
from .models import User, Category, Image, Article, ContentUnit
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.template.defaulttags import register
import json



# Create your views here.
def index(request):
    #message = os.environ['TEST_ENV_VAR']
    #return HttpResponse(message)
    #return HttpResponse('Hello World!')

    categories =  Category.objects.all().filter(is_active=True).order_by('display_order')
    return render(request, "drinx/index.html", {
        "categories": categories,
        "cartQty": cartQty(request)
    })

def articles(request, category_id):
    
    categories =  Category.objects.all().filter(is_active=True).order_by('display_order')
    if category_id == 0:
       articles =  Article.objects.all().filter(is_active=True).order_by('id')
    else:
        articles =  Article.objects.all().filter(categories=category_id, is_active=True).order_by('id')
    

    return render(request, "drinx/articles.html", {
        "articles" : articles,
        "categories": categories,
        "cartQty": cartQty(request)
    })

def cart(request):
    
    categories =  Category.objects.all().filter(is_active=True).order_by('display_order')
    
    # get all articles that are in the cart and convert it to a dictionary
    if "cart" not in request.session:
        cartItems = []
    else:
        cartItems = list(request.session["cart"])
    articlesInCartObj = Article.objects.filter(pk__in=cartItems)
    articlesInCart = {
        article.id: {
            "name": article.name,
            "price": float(article.price),
            "image": article.image,
            "cartQty": int(request.session["cart"][str(article.id)]),
            "totalPrice": float(article.price) * int(request.session["cart"][str(article.id)])
        }
        for article in articlesInCartObj
    }
    grandTotal = sum(articlesInCart[article]["price"]* articlesInCart[article]["cartQty"]\
                    for article in articlesInCart)
    
    return render(request, "drinx/cart.html", {
        "categories": categories,
        "cartQty": cartQty(request),
        "articlesInCart": articlesInCart,
        "grandTotal": grandTotal
    })

def login_view(request):
    
    categories =  Category.objects.all().filter(is_active=True).order_by('display_order')
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
                    "message": "Invalid email and/or password.",
                    "categories": categories,
                    "cartQty": cartQty(request)
                })
    else:
        return render(request, "drinx/login.html", {
            "categories": categories,
            "cartQty": cartQty(request)
        })

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

    categories =  Category.objects.all().order_by('id')

    return render(request, "drinx/backend_categories.html", {
        "categories" : categories
    })


@staff_member_required
def backend_articles(request, category_id):

    if request.method == 'POST' and request.FILES['filename']:
        #myimage = Image(image_large=request.FILES['filename'])
        #myimage.save()
        """
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        """
        #return render(request, "drinx/backend_articles.html", {
        #    'myimage': myimage.image_large
        #})

    units =  ContentUnit.objects.all().order_by('id')
    categories = Category.objects.all().order_by('id')

    if category_id == 0:
        articles =  Article.objects.all().order_by('name')
    else:
        articles = Article.objects.all().filter(categories__id=category_id).order_by('name')

    return render(request, "drinx/backend_articles.html", {
        "articles" : articles,
        "units": units,
        "categories": categories
    })


# API views

@csrf_exempt
@staff_member_required
def savecategory(request):

    # saving must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # get the data
    data = json.loads(request.body)
    action = data.get("action")
    id = data.get("id")
    name = data.get("name")
    description = data.get("description")
    is_active = data.get("is_active") or False
    display_order = data.get("display_order")

    try:
            if action == "update":
                category = Category.objects.get(id=id)
                category.name = name
                category.description = description
                category.is_active = is_active
                category.display_order = display_order
                category.save()
                return JsonResponse({
                            "message": "successfully updated",
                            },  status=201)
            elif action == "insert":
                category = Category(name=name, description=description, is_active=is_active, display_order=display_order)
                category.save()
                id=category.id
                return JsonResponse({
                            "message": "successfully new addded",
                            "newid": id
                            },  status=201)
            elif action == "delete":
                Category.objects.filter(id=id).delete()
                return JsonResponse({
                            "message": "successfully delted",
                            },  status=201)
            else: pass


    except Category.DoesNotExist:
        return JsonResponse({
            "error": f"Category with id {id} does not exist."
        }, status=400)


@csrf_exempt
@staff_member_required
def articleAPI(request):

    # saving must be via POST
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)
    try:
        article_id = request.GET["article_id"]

        # fetch the article
        article = Article.objects.get(id=article_id)
        
        # serialize the response to JSON
        article_data = serializers.serialize('json', [article, ])
        struct = json.loads(article_data)
        article_data = json.dumps(struct[0])
            
        return HttpResponse(article_data, status=201)
    
    except Article.DoesNotExist:
        return JsonResponse({
            "error": f"Article with id {id} does not exist."
        }, status=400)


@csrf_exempt
def cartAPI(request):

    # saving must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    try:
        # get the article id and qty from the request that shall be pushed to the cart
        article_id = request.GET["articleId"]
        qty = request.GET["qty"]

        if not "cart" in request.session:
            request.session["cart"] = {}
        if int(qty) == 0:
            # dump from cart if qty is set to 0
            if article_id in request.session["cart"]:
                request.session["cart"].pop(article_id)
                request.session.modified = True
            return JsonResponse({
                    "message": "Article removed from cart.",
                    "cartArticleQty": 0, 
                    "cartQty": cartQty(request)
                }, status=201)
        else:
            # check if there is still enough stock available
            article = Article.objects.get(id=article_id)
            if article.stock < int(qty):
                return JsonResponse({
                    "message": "Not enough stock.",
                    "cartArticleQty": request.session["cart"].get(article_id), 
                    "cartQty": cartQty(request)
                }, status=202)
            else:
                if article_id in request.session["cart"]:
                    # article is already in the cart then add the quantity to the existing one
                    oldQty = request.session["cart"][article_id]
                    request.session["cart"].update({
                        article_id: int(qty) + int(oldQty)
                    })
                else:
                    # if article is not yet in the cart
                    request.session["cart"].update({
                        article_id: qty
                    })
        request.session.modified = True       
        return JsonResponse({
            "message": "Cart updated.",
            "cartArticleQty": request.session["cart"].get(article_id), 
            "cartQty": cartQty(request)
        }, status=200)
    except :
        return JsonResponse({
            "error": "Server Error"
        }, status=400)


# Helper functions

# Function that retrieves the current quantity of items in the cart
def cartQty(request):
    cartQty = 0
    if "cart" not in request.session:
        return "empty"
    for item in request.session["cart"]:
        cartQty += int(request.session["cart"][item])
    if cartQty == 0:
        return "empty"
    else:
        return cartQty

# Function that allows to access a dictionary with attribute lookup in the template
@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key))

