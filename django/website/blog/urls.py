from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<slug:location>', views.HomeView.as_view(), name='home'),
    path('<slug:location>/<slug:service>', views.HomeView.as_view(), name='home'),
    path('quote', views.HomeView.as_view(), name='home'),
    path('contact', views.HomeView.as_view(), name='home'),
    path('about', views.HomeView.as_view(), name='home'),
    path('<int:int>/sitemap.xml.gz', views.sitemap, name='sitemap'),
    path('sitemap_index.xml', views.sitemap_index, name='sitemap_index')
]