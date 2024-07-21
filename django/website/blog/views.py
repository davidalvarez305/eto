from datetime import date, datetime
import os
from pathlib import Path
import tempfile
import uuid

from .landing_pages import LANDING_PAGES
from .forms import QuoteForm
from django.shortcuts import render, get_object_or_404
from django.views import View

from .utils import get_client_ip
from .google.gmail import EmailService
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.utils import timezone
from django.core.paginator import Paginator
import boto3

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
        'meta_description': 'Fumero Cleaning Services is a family-owned business servicing the entire South Florida area with high quality cleaning solutions from pressure washing, concrete, post-construction, and office cleaning!',
        'page_title': str(os.environ.get('SITE_NAME')),
        'site_name': str(os.environ.get('SITE_NAME')),
        'phone_number': '({}) - {} {}'.format(phone_number[:3], phone_number[3:6], phone_number[6:]),
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

class ServicesView(HomeView):
    template_name = 'blog/services.html'

class PrivacyPolicyView(HomeView):
    template_name = 'blog/privacy_policy.html'
    
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

class ContactView(MyBaseView):
    template_name = 'blog/contact.html'

    def get(self, request, *args, **kwargs):
        context = self.context
        context['page_path'] = request.build_absolute_uri()
        context['page_title'] = str(os.environ.get('SITE_NAME'))
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        try:
            form = request.POST.dict()
            email_service = EmailService()
            email_service.send_mail(form)
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
        data = request.POST.dict()
        form = QuoteForm(request.POST, request.FILES)
        email_service = EmailService()
        if form.is_valid():
            try:
                user_ip = get_client_ip(request)
                
                location = Location.objects.get(id=data.get('location'))
                service = Service.objects.get(id=data.get('service'))

                with transaction.atomic():
                    lead = Lead.objects.create(
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                        phone_number=form.cleaned_data['phone_number'],
                        message=form.cleaned_data['message'],
                        location=location,
                        service=service,
                        latitude=float(data.get('latitude')),
                        longitude=float(data.get('longitude')),
                        date_created=timezone.now()
                    )

                    marketing = Marketing.objects.create(
                        lead=lead,
                        landing_page=data.get('landing_page'),
                        referrer=data.get('referrer'),
                        keyword = data.get('keyword'),
                        channel = data.get('channel'),
                        source = data.get('source'),
                        medium = data.get('medium'),
                        ad_campaign = data.get('ad_campaign'),
                        ad_group = data.get('ad_group'),
                        ad_headline = data.get('ad_headline'),
                        gclid = data.get('gclid'),
                        language = data.get('language'),
                        user_agent = data.get('userAgent'),
                        button_clicked = data.get('button_clicked'),
                        lead_channel = data.get('lead_channel'),
                        ip = user_ip
                    )

                    for file_to_upload in request.FILES.getlist('file_upload'):
                        # Upload Image to S3
                        ext = Path(file_to_upload.name).suffix
                        img_file_name = str(uuid.uuid4()) + ext
                        s3_upload_path = f'images/{img_file_name}'
                        s3 = boto3.client('s3')

                        # Create a temporary file to save the uploaded image
                        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                            for chunk in file_to_upload.chunks():
                                temp_file.write(chunk)

                            temp_file.close()

                            s3.upload_file(temp_file.name, os.environ.get('AWS_STORAGE_BUCKET_NAME'), s3_upload_path)

                            os.unlink(temp_file.name)

                            # Save Image to DB
                            LeadImage.objects.create(
                                lead=lead,
                                src=img_file_name
                            )

                    marketing.save()

                    qs = LeadImage.objects.filter(lead_id=lead.id)
                    lead_images = list(qs)

                    # Send Email Notification
                    email_service.lead_notification(lead, lead_images)

                return JsonResponse({ "data": "Contact form received successfully." }, status=201)
            except Exception as e:
                print("Error:", e)
                return JsonResponse({ "data": "Failed to create lead." }, status=500)
        else:
            return JsonResponse({ "data": "Form was not submitted successfully." }, status=400)

class PPCLandingPageView(MyBaseView):
    template_name = 'blog/ppc.html'

    def get(self, request, *args, **kwargs):
        context = self.context
        service = self.kwargs.get('slug')
        ppc_context = LANDING_PAGES.get(service)

        if ppc_context is None:
            return HttpResponseBadRequest("Page not found.")

        context['page_title'] = ppc_context.get('title') + " - " + str(os.environ.get('SITE_NAME'))
        context['h1'] = ppc_context.get('h1')

        context['page_path'] = request.build_absolute_uri()
        return render(request, self.template_name, context=context)

class LeadsView(LoginRequiredMixin, MyBaseView):
    template_name = 'blog/leads.html'
    login_url="/login"

    def get(self, request, *args, **kwargs):
        context = self.context
        params = request.GET.dict()
        filters = {}
        LIMIT_VALUE = 5

        # Handle page
        page_qs = params.pop('page', '1')
        page = int(page_qs)

        # Handle date
        dates = params.pop('date_filter', '')

        if len(dates) > 0:
            start_date_str, end_date_str = dates.split(" to ")

            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            filters['date_created__range'] = [start_date, end_date]

        # Handle phone number
        phone_number = params.pop('phone_number', '')
        if len(phone_number) > 0:
            filters['phone_number'] = phone_number
        
        # Handle location
        location_id = params.pop('location_id', '')
        if len(location_id) > 0:
            filters['location_id'] = location_id
        
        # Handle service
        service_id = params.pop('service_id', '')
        if len(service_id) > 0:
            filters['service_id'] = service_id

        leads = Lead.objects.prefetch_related('marketing_set').filter(**filters).order_by('-date_created')
        services = Service.objects.all()
        locations = Location.objects.all()

        paginator = Paginator(leads, LIMIT_VALUE)
        data = paginator.get_page(page)

        photos_dict = {}
        for lead in leads:
            if (lead.images.count() > 0):
                photos_dict[lead.id] = [image.src for image in lead.images.all()]

        context['is_leads'] = True
        context['leads'] = data
        context['current_page'] = data.number
        context['max_page'] = data.paginator.num_pages
        context['services'] = services
        context['locations'] = locations
        context['page_path'] = request.build_absolute_uri()
        context['page_title'] = str(os.environ.get('SITE_NAME'))
        return render(request, self.template_name, context=context)

class LeadDetailView(LoginRequiredMixin, MyBaseView):
    template_name = 'blog/lead_detail.html'
    login_url="/login"

    def get(self, request, *args, **kwargs):
        context = self.context
        id = kwargs.get('id')
        lead = get_object_or_404(Lead.objects.prefetch_related('marketing_set'), id=id)
        services = Service.objects.all()
        locations = Location.objects.all()

        context['is_leads'] = True
        context['lead'] = lead
        context['services'] = services
        context['locations'] = locations
        context['page_path'] = request.build_absolute_uri()
        context['page_title'] = str(os.environ.get('SITE_NAME'))
        context['lead_images'] = [image.src for image in lead.images.all()]
        return render(request, self.template_name, context=context)

class LeadImagesList(View):
    template_name = 'blog/photos.html'

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')

        if not id:
            return HttpResponseBadRequest("No lead_id provided.")

        try:
            lead_images = LeadImage.objects.filter(lead_id=id)
        except LeadImage.DoesNotExist:
            lead_images = []
        
        bucket_url = "https://" + os.environ.get('AWS_STORAGE_BUCKET_NAME') + ".s3.amazonaws.com/images/"

        html_content = ''
        for image in lead_images:
            html_content += f'<div><img src="{bucket_url}{image.src}" /></div>'

        return HttpResponse(html_content)
