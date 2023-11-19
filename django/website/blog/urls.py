from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<slug:location>', views.HomeView.as_view(), name='location'),
    path('<slug:location>/<slug:service>', views.ServiceLocationView.as_view(), name='service_location'),
    path('quote', views.HomeView.as_view(), name='quote'),
    path('contact', views.HomeView.as_view(), name='contact'),
    path('about', views.HomeView.as_view(), name='about'),
    path('<int:int>/sitemap.xml.gz', views.sitemap, name='sitemap'),
    path('sitemap_index.xml', views.sitemap_index, name='sitemap_index')
]