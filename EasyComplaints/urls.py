"""
URL configuration for EasyComplaints project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path
from login_and_signup.views import *
from Dashboard.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    
    path('', home_page, name='home_page'),
    path('admin/', admin.site.urls),
    path('login/', user_login, name='user_login'),
    path('register/', citizen_registration, name='register'),
    path('dashboard/',dashboard, name='dashboard'),
    path('new-complaint/', new_complaint, name='new_complaint'),
    path('complaints/<int:id>/',department_complaints, name='department_complaints'),
    path('logout/', user_logout, name='user_logout'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)