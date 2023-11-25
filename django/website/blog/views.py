from datetime import date, datetime
import json
import mimetypes
import os
import uuid
from .forms import QuoteForm
import httpagentparser
from django.shortcuts import render
from django.views import View

from .utils import download_image, get_client_ip, get_device_type, get_exif_data, remove_files_in_directory, resolve_uploads_dir_path, scan_for_viruses, send_message_with_twilio, upload_to_s3
from .google.gmail import send_mail
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.utils import timezone
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse

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
                device_data = httpagentparser.detect(data.get('userAgent'))
                user_os = device_data['os']['name']
                device_type = get_device_type(device_data)
                
                location = Location.objects.get(id=data['location'])
                service = Service.objects.get(id=data['service'])

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
                        os = user_os,
                        user_agent = data.get('userAgent'),
                        button_clicked = data.get('button_clicked'),
                        lead_channel = data.get('lead_channel'),
                        device_type = device_type,
                        ip = user_ip
                    )

                    marketing.save()

                    # Send client text message letting them know they can upload pictures.
                    send_message_with_twilio(message=f"""
                        Hey! Thank you for requesting a quote from Fumero Cleaning Services, LLC.
                        This is a text message to let you know that you can send pictures through here & we'll attach them to your account!
                    """, to_phone_number=form.cleaned_data['phone_number'])

                return JsonResponse({ "data": "Contact form received successfully." }, status=201)
            except Exception as e:
                print("Error:", str(e))
                return JsonResponse({ "data": "Failed to create lead." }, status=500)
        else:
            return JsonResponse({ "data": "Form was not submitted successfully." }, status=400)

class PPCLandingPageView(MyBaseView):
    template_name = 'blog/pressure_washing.html'

    def get(self, request, *args, **kwargs):
        context = self.context
        context['page_path'] = request.build_absolute_uri()
        context['page_title'] = 'Pressure Washing in Miami, FL - ' + str(os.environ.get('SITE_NAME'))
        return render(request, self.template_name, context=context)

class LeadsView(MyBaseView):
    template_name = 'blog/leads.html'

    def get(self, request, *args, **kwargs):
        context = self.context
        params = request.GET.dict()

        # Remove page from querystring
        page = params.pop('page', None)
        limit_value = 25

        if page is None:
            page = 1
        else:
            # Transform querystring to int
            page = int(page)

        # Remove date from querystring
        dates = params.pop('date_filter', None)

        if dates is not None:
            start_date_str, end_date_str = dates.split(" to ")

            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            params['date_created__range'] = [start_date, end_date]

        leads = Lead.objects.filter(**params).order_by('-date_created')
        services = Service.objects.all()
        locations = Location.objects.all()

        paginator = Paginator(leads, limit_value)
        max_pages = paginator.num_pages
        data = paginator.get_page(page)

        context['is_leads'] = True
        context['leads'] = data
        context['max_pages'] = max_pages
        context['min_page'] = page
        context['num_pages'] = [x for x in range(page + 1, page + 5) if x <= max_pages]
        context['services'] = services
        context['locations'] = locations
        context['page_path'] = request.build_absolute_uri()
        context['page_title'] = str(os.environ.get('SITE_NAME'))
        return render(request, self.template_name, context=context)
    
@csrf_exempt
def handle_incoming_message(request):
    try:
        message_sid = request.POST.get('MessageSid', '')
        client_phone_number = request.POST.get('From', '')
        num_media = int(request.POST.get('NumMedia', 0))

        media_files = [(request.POST.get("MediaUrl{}".format(i), ''),
                        request.POST.get("MediaContentType{}".format(i), ''))
                    for i in range(0, num_media)]
        
        for file in media_files:
            url, file_extension = file
            
            if "image" in file_extension:

                # Resolve image path
                ext = mimetypes.guess_extension(file_extension)
                img_file_name = uuid.uuid4()
                uploads_dir = resolve_uploads_dir_path()
                image_file_path = uploads_dir + "/" + str(img_file_name) + ext

                # Download image locally
                download_image(url, image_file_path)

                # Get GPS Info
                get_exif_data(image_file_path)

                # Scan for viruses
                # scan_for_viruses(image_file_path)
        
        
                # Upload Image to S3
                s3_upload_path = f'images/{str(img_file_name)}{ext}'
                upload_to_s3(local_file_path=image_file_path, bucket_name=os.environ.get('AWS_STORAGE_BUCKET_NAME'), s3_file_name=s3_upload_path)
                
                # Save Image to DB
                adjusted_phone_number = client_phone_number.split("+1")[1]
                lead = Lead.objects.get(phone_number=adjusted_phone_number)
                LeadImage.objects.create(
                    lead=lead,
                    src=str(img_file_name) + ext
                )
                print("Image successfully added to DB.")

                send_message_with_twilio(message='Your {} images have been successfully uploaded!'.format(num_media), to_phone_number=client_phone_number)
                print("Client received response.")
        
        return HttpResponse("", content_type='application/xml')
    except Exception as err:
        print(f'ERROR IN TWILIO WEBHOOK: {err}')
        return HttpResponseBadRequest('Upload failed.')
    finally:
        remove_files_in_directory(uploads_dir)