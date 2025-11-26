from django.shortcuts import render, redirect
import requests
from datetime import datetime, date
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth import logout, authenticate , login 
from home.models import Contact, Order
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from django.urls import reverse_lazy
import os
from django.core.cache import cache
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .email_utils import (
    send_welcome_email, 
    send_order_confirmation_email, 
    send_contact_confirmation_email
)
from django_ratelimit.decorators import ratelimit
from .audit_utils import log_activity
from django.db.models import Q
from django.http import JsonResponse

API_KEY = os.getenv('PEXELS_API_KEY', 'lwDW7CBQoNtS0iOxfGSzD2wQvnaAuGo7ikma5d2FPnBt7KrNPxqBDHVQ') 

def fetch_random_images(query, num_images=8):
    """Fetch random images from Pexels API based on a query with caching."""
    # Create a cache-safe key by replacing spaces and special characters
    cache_key = f'pexels_images_{query.replace(" ", "_")}_{num_images}'
    images = cache.get(cache_key)
    
    if images is not None:
        return images
    
    url = f'https://api.pexels.com/v1/search?query={query}&per_page={num_images}&page=1'
    headers = {
        'Authorization': API_KEY
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        images = [photo['src']['original'] for photo in data['photos']]
        cache.set(cache_key, images, settings.API_CACHE_TIMEOUT)
        return images
    except requests.RequestException as e:
        messages.error(None, f"Could not fetch images from Pexels: {str(e)}")
        return [] 

def home(request):
    theme = "textile industry" 
    random_images = fetch_random_images(theme)
    if request.user.is_anonymous:
        return redirect(reverse_lazy('login'))
    return render(request, 'index.html', {'random_images': random_images})

def about(request):
    theme = "thread" 
    random_images = fetch_random_images(theme)
    return render(request, 'about.html', {'random_images': random_images})


def services(request):
    """Display services page with configurable content."""
    from home.models import ServicePage, PartnerLogo
    
    # Get or create service page content
    service_page, created = ServicePage.objects.get_or_create(
        defaults={
            'title': 'Our Partners',
            'heading': "Let's Collaborate",
            'content': '''At Enterprises, we take pride in being the trusted thread supplier for leading brands such as Nishat Linen, Shahkam Industries, Outfitters, Leisure Club, Sadaqat Limited, Serena Fabrics, and Ayesha Fabrics. Whether for export or local production, we are dedicated to delivering high-quality thread in bulk or tailored to your specific requirements. Our commitment to timely delivery ensures that our partners receive their materials on schedule, every time, anywhere in Pakistan.

If you seek to establish a strategic partnership with a reliable supplier committed to excellence and customer satisfaction, we welcome the opportunity to connect. Our team is ready to discuss how we can provide customized solutions that align with your operational needs and enhance your product offerings.'''
        }
    )
    
    # Get active partner logos
    partner_logos = PartnerLogo.objects.filter(is_active=True).order_by('order')
    
    return render(request, 'services.html', {
        'service_page': service_page,
        'partner_logos': partner_logos
    })

@login_required(login_url='/login/')
def status(request):
    """Display user's order history with status tracking and pagination."""
    orders_list = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Pagination - 15 orders per page
    paginator = Paginator(orders_list, 15)
    page = request.GET.get('page', 1)
    
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        orders = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        orders = paginator.page(paginator.num_pages)
    
    return render(request, 'status.html', {'orders': orders})

from .forms import OrderForm

@ratelimit(key='user', rate='20/h', method='POST', block=True)
def orders(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login'))
    
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user  # Link order to user
            order.save()
            
            # Send order confirmation email
            send_order_confirmation_email(order, request)
            
            messages.success(request, f'Dear {request.user}, your order has been placed. A confirmation email has been sent.')
            return redirect('orders')
        else:
            messages.error(request, "Please correct the errors in the form")
    else:
        form = OrderForm()
    
    return render(request, 'orders.html', {'form': form})



def success(request):
 
   return render(request, 'success.html')  # Ensure you have a success.html file


@login_required
@ratelimit(key='ip', rate='10/h', method='POST', block=True)
def contact(request):
    theme = "contact" 
    random_images = fetch_random_images(theme) 

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        
        # Basic validation
        if not all([name, email, phone, desc]):
            messages.error(request, "All fields are required.")
            return render(request, 'contact.html', {'random_images': random_images})
        
        try:
            contact = Contact(
                user=request.user,  # Added user relationship
                name=name,
                email=email,
                phone=phone,
                desc=desc,
                date=date.today()
            )
            contact.full_clean()  # Validate model
            contact.save()
            
            # Log contact form submission
            log_activity(
                user=request.user,
                action='contact_submitted',
                description=f'Contact form submitted by {request.user.username}',
                request=request,
                content_type='Contact',
                object_id=contact.id
            )
            
            # Send confirmation email
            send_contact_confirmation_email(contact)
            
            # Handle AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Your message has been sent. A confirmation email has been sent to you.'
                })
            
            messages.success(request, "Your message has been sent. A confirmation email has been sent to you.")
            return redirect(reverse_lazy('contact'))
        except Exception as e:
            # Handle AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'There was an error sending your message. Please try again.',
                    'errors': {'__all__': [str(e)]}
                })
            
            messages.error(request, "There was an error sending your message. Please try again.")
            return render(request, 'contact.html', {'random_images': random_images})

    return render(request, 'contact.html', {'random_images': random_images})

@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def loginUser(request):
    if request.method == 'POST':
        # Checking if user has entered correct credentials
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        
        user = authenticate(username=username, password=password) 
        if user is not None:
            login(request, user)
            
            # Handle Remember Me functionality
            if remember_me:
                # Keep session for 2 weeks (1209600 seconds)
                request.session.set_expiry(1209600)
            else:
                # Session expires when browser closes
                request.session.set_expiry(0)
            
            return redirect(reverse_lazy('home'))  
        else:
       
            messages.error(request, "Invalid username or password")
            return render(request, 'login.html')
    return render(request, 'login.html')

def logoutuser(request):
    logout(request)
    return redirect(reverse_lazy('login'))

@ratelimit(key='ip', rate='3/m', method='POST', block=True)
def signupUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Basic validation
        if not all([username, email, password, confirm_password]):
            messages.error(request, "All fields are required!")
            return render(request, 'signup.html')

        # Checking if the passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'signup.html')

        # Validate email format
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email format!")
            return render(request, 'signup.html')

        # Password strength validation
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long!")
            return render(request, 'signup.html')

        try:
            # Checking if the username or email already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken!")
                return render(request, 'signup.html')

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already in use!")
                return render(request, 'signup.html')

            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # Send welcome email
            send_welcome_email(user, request)

            # Authenticate and log in the user
            login(request, user)
            messages.success(request, "Your account has been created successfully! Check your email for a welcome message.")
            return redirect('/')
        except Exception as e:
            messages.error(request, "There was an error creating your account. Please try again.")
            return render(request, 'signup.html')

    return render(request, 'signup.html')
@login_required(login_url='/login/')
def profile(request):
    """Display user profile information."""
    theme = "user profile"
    random_images = fetch_random_images(theme, num_images=3)
    return render(request, 'profile.html', {
        'random_images': random_images,
        'user': request.user
    })

@login_required(login_url='/login/')
def edit_profile(request):
    """Edit user profile information."""
    if request.method == 'POST':
        try:
            user = request.user
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip()
            
            # Validate email
            if not email:
                messages.error(request, "Email is required!")
                return redirect('edit_profile')
            
            # Check if email is already taken by another user
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                messages.error(request, "This email is already in use by another account!")
                return redirect('edit_profile')
            
            # Update user information
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            
            # Log profile update
            log_activity(
                user=user,
                action='profile_update',
                description=f'Profile updated: {user.username}',
                request=request
            )
            
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile')
        except Exception as e:
            messages.error(request, f"Error updating profile: {str(e)}")
            return redirect('edit_profile')
    
    theme = "edit profile"
    random_images = fetch_random_images(theme, num_images=3)
    return render(request, 'edit_profile.html', {
        'random_images': random_images,
        'user': request.user
    })

@login_required(login_url='/login/')
def change_password(request):
    """Change user password."""
    if request.method == 'POST':
        try:
            user = request.user
            current_password = request.POST.get('current_password', '')
            new_password = request.POST.get('new_password', '')
            confirm_password = request.POST.get('confirm_password', '')
            
            # Verify current password
            if not user.check_password(current_password):
                messages.error(request, "Current password is incorrect!")
                return redirect('change_password')
            
            # Validate new password
            if len(new_password) < 8:
                messages.error(request, "New password must be at least 8 characters long!")
                return redirect('change_password')
            
            if new_password != confirm_password:
                messages.error(request, "New passwords do not match!")
                return redirect('change_password')
            
            # Password strength check
            if new_password.isdigit():
                messages.error(request, "Password cannot be entirely numeric!")
                return redirect('change_password')
            
            # Update password
            user.set_password(new_password)
            user.save()
            
            # Log password change
            log_activity(
                user=user,
                action='password_change',
                description=f'Password changed for user: {user.username}',
                request=request
            )
            
            # Re-authenticate user to keep them logged in
            login(request, user)
            
            messages.success(request, "Your password has been changed successfully!")
            return redirect('profile')
        except Exception as e:
            messages.error(request, f"Error changing password: {str(e)}")
            return redirect('change_password')
    
    theme = "security"
    random_images = fetch_random_images(theme, num_images=3)
    return render(request, 'change_password.html', {
        'random_images': random_images
    })


def ratelimit_error(request, exception=None):
    """Custom view for rate limit exceeded errors."""
    return render(request, 'ratelimit.html', status=429)


@login_required(login_url='/login/')
def search(request):
    """Search for orders by title, client name, or description."""
    query = request.GET.get('q', '').strip()
    orders_list = []
    
    if query:
        # Search across multiple fields using Q objects
        orders_list = Order.objects.filter(
            Q(user=request.user) &  # Only show user's own orders
            (
                Q(title__icontains=query) |
                Q(client_name__icontains=query) |
                Q(description__icontains=query) |
                Q(status__icontains=query) |
                Q(priority__icontains=query)
            )
        ).order_by('-created_at')
    
    # Pagination - 15 results per page
    paginator = Paginator(orders_list, 15)
    page = request.GET.get('page', 1)
    
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    
    context = {
        'orders': orders,
        'query': query,
        'total_results': orders_list.count() if query else 0
    }
    
    return render(request, 'search.html', context)

