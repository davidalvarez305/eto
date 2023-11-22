from datetime import date
import json
import math
import os
from .forms import QuoteForm
import httpagentparser
from django.shortcuts import render
from django.views import View

from .utils import get_client_ip, get_device_type
from .google.gmail import send_mail
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout

class MyBaseView(View):
    domain = str(os.environ.get('DJANGO_DOMAIN'))
    current_year = date.today().year
    google_analytics_id = str(os.environ.get('GOOGLE_ANALYTICS_ID'))
    phone_number = str(os.environ.get('PHONE_NUMBER'))

    context = {
        'domain': domain,
        'current_year': current_year,
        'google_analytics_id': google_analytics_id,
        'google_analytics_src': "https://www.googletagmanager.com/gtag/js?id=" + google_analytics_id,
        'meta_description': 'Get reviews for all things sports, fitness, outdoors, and everything in between!',
        'page_title': str(os.environ.get('SITE_NAME')),
        'site_name': str(os.environ.get('SITE_NAME')),
        'phone_number': '({}) - {} {}'.format(phone_number[:3], phone_number[3:6], phone_number[6:]),
        'is_reviewpost': False,
    }

    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context=self.context)

class HomeView(MyBaseView):
    template_name = 'blog/home.html'

    def get(self, request, *args, **kwargs):
        context = self.context
        context['page_path'] = request.build_absolute_uri()
        context['page_title'] = str(os.environ.get('SITE_NAME'))
        return render(request, self.template_name, context=context)
    
class Login(MyBaseView):
    template_name = 'blog/login.html'

    def get(self, request, *args, **kwargs):
        context = self.context
        context['page_path'] = request.build_absolute_uri()
        context['page_title'] = str(os.environ.get('SITE_NAME'))
        return render(request, self.template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        form = request.POST.dict()
        user = authenticate(request=request, username=form.get('username'), password=form.get('password'))

        if user is not None:
            login(request, user)
            return JsonResponse({ 'data': 'Success.'}, status=200)
        else:
            return JsonResponse({ 'data': 'Authentication failed.'}, status=400)
        
class Logout(MyBaseView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return JsonResponse({ 'data': 'Logged out.'}, status=200)

class ContactView(MyBaseView):
    template_name = 'blog/contact.html'

    def get(self, request, *args, **kwargs):
        context = self.context
        context['page_path'] = request.build_absolute_uri()
        context['page_title'] = str(os.environ.get('SITE_NAME'))
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            send_mail(data)
            return JsonResponse({ "data": "Contact form received successfully." })
        except Exception as e:
            print("Error:", str(e))
            return JsonResponse({ "data": "Failed to parse request body." }, status=400)

class QuoteView(MyBaseView):
    template_name = 'blog/quote.html'

    def get(self, request, *args, **kwargs):
        context = self.context

        services = Service.objects.all()
        locations = Location.objects.all()

        context['page_path'] = request.build_absolute_uri()
        context['page_title'] = str(os.environ.get('SITE_NAME'))
        context['services'] = list(services.values())
        context['locations'] = list(locations.values())
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        form = QuoteForm(data)
        if form.is_valid():
            try:
                user_ip = get_client_ip(request)
                device_data = httpagentparser.detect(data['userAgent'])
                user_os = device_data['os']['name']
                device_type = get_device_type(device_data)
                print(data)
                print(user_ip)
                print(user_os)
                print(device_type)
                return JsonResponse({ "data": "Contact form received successfully." })
            except Exception as e:
                print("Error:", str(e))
                return JsonResponse({ "data": "Failed to parse request body." }, status=400)
        else:
            return JsonResponse({ "data": "Form was not submitted successfully." }, status=400)

class PPCLandingPageView(MyBaseView):
    template_name = 'blog/pressure_washing.html'

    def get(self, request, *args, **kwargs):
        context = self.context
        context['page_path'] = request.build_absolute_uri()
        context['page_title'] = 'Pressure Washing in Miami, FL - ' + str(os.environ.get('SITE_NAME'))
        return render(request, self.template_name, context=context)