from django.shortcuts import render, redirect
import requests
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth import logout, authenticate , login 
from home.models import Contact, Order




API_KEY = 'lwDW7CBQoNtS0iOxfGSzD2wQvnaAuGo7ikma5d2FPnBt7KrNPxqBDHVQ' 

def fetch_random_images(query, num_images=8):
    """Fetch random images from Pexels API based on a query."""
    url = f'https://api.pexels.com/v1/search?query={query}&per_page={num_images}&page=1'
    headers = {
        'Authorization': API_KEY
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return [photo['src']['original'] for photo in data['photos']]
    else:
        messages.error("Could not fetch images from Pexels.")  # type: ignore
        return [] 

def home(request):
    theme = "textile industry" 
    random_images = fetch_random_images(theme)
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request, 'index.html', {'random_images': random_images})

def about(request):
    theme = "thread" 
    random_images = fetch_random_images(theme)
    return render(request, 'about.html', {'random_images': random_images})


def services(request):
    return render(request, 'services.html')

def status(request):
    return render(request, 'status.html')

def orders(request):
    theme = "order"  
    random_images = fetch_random_images(theme)  
    if request.method == 'POST':
        client_name = request.POST.get('client_name')
        description = request.POST.get('description')
        title = request.POST.get('title')
        priority = request.POST.get('priority')
        quantity = request.POST.get('quantity')
        order = Order(client_name=client_name, description=description,
                       title=title, priority=priority, quantity=quantity)
        order.save()
        messages.success(request, 'Dear {{request.user}}your order has been placed')
        return render(request, 'orders.html', {'random_images' : random_images})
    else:
        messages.error(request, "There was an error with your order form.")
    return render(request, 'orders.html', {'random_images' : random_images})




def success(request):
    return render(request, 'success.html')  # Ensure you have a success.html file
def contact(request):
    theme = "contact" 
    random_images = fetch_random_images(theme) 

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        
   
        contact = Contact(name=name, email=email, phone=phone, desc=desc, date=datetime.today())
        contact.save()


        messages.success(request, "Your message has been sent")
        
        return render(request, 'contact.html', {'random_images': random_images})  # Pass images to the template again after submission

    return render(request, 'contact.html', {'random_images': random_images})  # Pass images to the template
def loginUser(request):
    if request.method == 'POST':
        # Checking if user has entered correct credentials
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password) 
        if user is not None:
            login(request, user)
            return redirect("/")  
        else:
       
            messages.error(request, "Invalid username or password")
            return render(request, 'login.html')
    return render(request, 'login.html')

def logoutuser(request):
    logout(request)
    return redirect("/login")

def signupUser(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Checking if the passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'signup.html')

        # Checking if the username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return render(request, 'signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use!")
            return render(request, 'signup.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Authenticate and log in the user
        login(request, user)
        messages.success(request, "Your account has been created successfully!")
        return redirect('/')

    return render(request, 'signup.html')