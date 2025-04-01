from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from accounts.views import dashboard

# Function to redirect '/' to '/login/'
def home_redirect(request):
    return redirect('login_selection')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_redirect, name='home'),  # Redirect root URL to login
    path('accounts/', include('accounts.urls')),  # Include accounts URLs
    path('dashboard/',dashboard,name='dashboard'),
]
