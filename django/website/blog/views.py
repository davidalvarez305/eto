from datetime import date, datetime
import json
import mimetypes
import os
import uuid

from .google.google_analytics import track_conversion

from .landing_pages import LANDING_PAGES
from .forms import QuoteForm
import httpagentparser
from django.shortcuts import render
from django.views import View

from .utils import download_image, get_client_ip, get_device_type, get_exif_data, remove_files_in_directory, resolve_uploads_dir_path, scan_for_viruses, upload_to_s3
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
from twilio.twiml.voice_response import VoiceResponse

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
                device_data = httpagentparser.detect(data.get('userAgent'), '')
                device_type = get_device_type(device_data)

                user_os = ''
                device_os = device_data.get('os', None)
                if device_os is not None:
                    user_os = device_os.get('name', '')
                
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

        # Remove page from querystring
        page = params.pop('page', None)
        limit_value = 2

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

        leads = Lead.objects.prefetch_related('marketing_set').filter(**params).order_by('-date_created')
        services = Service.objects.all()
        locations = Location.objects.all()

        paginator = Paginator(leads, limit_value)
        data = paginator.get_page(page)

        current_page = data.number
        min_page = max(current_page - 2, data.paginator.page_range[0])
        max_page = min(current_page + 2, data.paginator.page_range[-1])

        photos_dict = {}
        for lead in leads:
            if (lead.images.count() > 0):
                photos_dict[lead.id] = [image.src for image in lead.images.all()]

        active_hover = "paginationAnchor hover:cursor-pointer -mr-px inline-flex items-center justify-center space-x-2 border border-gray-200 bg-gray-100 px-4 py-2 font-semibold leading-6 text-gray-800 hover:z-1 hover:border-gray-300 hover:text-gray-900 hover:shadow-sm focus:z-1 focus:ring focus:ring-gray-300 focus:ring-opacity-25 active:z-1 active:border-gray-200 active:shadow-none dark:border-gray-700 dark:bg-gray-700/75 dark:text-gray-300 dark:hover:border-gray-600 dark:hover:text-gray-200 dark:focus:ring-gray-600 dark:focus:ring-opacity-40 dark:active:border-gray-700"
        non_active_hover = "paginationAnchor hover:cursor-pointer -mr-px inline-flex items-center justify-center space-x-2 border border-gray-200 bg-white px-4 py-2 font-semibold leading-6 text-gray-800 hover:z-1 hover:border-gray-300 hover:text-gray-900 hover:shadow-sm focus:z-1 focus:ring focus:ring-gray-300 focus:ring-opacity-25 active:z-1 active:border-gray-200 active:shadow-none dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:border-gray-600 dark:hover:text-gray-200 dark:focus:ring-gray-600 dark:focus:ring-opacity-40 dark:active:border-gray-700"
        
        context['is_leads'] = True
        context['leads'] = data
        context['active_hover'] = active_hover
        context['non_active_hover'] = non_active_hover
        context['current_page'] = current_page
        context['max_pages'] = max_page
        context['min_page'] = min_page
        context['num_pages'] = [x for x in range(min_page, page + 5) if x <= max_page]
        context['services'] = services
        context['locations'] = locations
        context['page_path'] = request.build_absolute_uri()
        context['page_title'] = str(os.environ.get('SITE_NAME'))
        context['photos_dict'] = photos_dict
        context['bucket_url'] = "https://" + os.environ.get('AWS_STORAGE_BUCKET_NAME') + ".s3.amazonaws.com/images/" # I can change this later to pull from CUSTOM DOMAIN
        return render(request, self.template_name, context=context)

@csrf_exempt
def handle_incoming_call(request):
    try:
        msg_body = request.POST.dict()
        destination_phone_number = os.environ.get('TO_PHONE_NUMBER')
        caller_id = msg_body.get('Caller', None)

        if caller_id is None:
            return HttpResponseBadRequest('Invalid caller ID.')

        response = VoiceResponse()
        dial = response.dial(caller_id=caller_id)
        dial.number(destination_phone_number)

        track_conversion()
        return HttpResponse(str(response), content_type='application/xml')
    except BaseException as e:
        print(f'Error handling incoming phone call: {e}')

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
        
        return HttpResponse("", content_type='application/xml')
    except Exception as err:
        print(f'ERROR IN TWILIO WEBHOOK: {err}')
        return HttpResponseBadRequest('Upload failed.')
    finally:
        remove_files_in_directory(uploads_dir)