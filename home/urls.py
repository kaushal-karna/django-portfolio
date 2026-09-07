from django.urls import path
from . import views

urlpatterns = [      
            path('home/', views.home, name='home'),
            path('', views.homepage, name="homepage"),  # Landing page
            path('about/', views.about, name='about'),
            path('contact/', views.contact, name='contact'),
            path('blog/', views.blog, name = 'blog'),
            path('experience/', views.experience, name='experience'),
            path('certifications/', views.certification, name='certification')
        
            
]