from django.db import models

class SEO(models.Model):
    title = models.CharField(max_length=255, null=True)
    meta_description = models.TextField(null=True)
    slug = models.SlugField(db_index=True, unique=True)
    content = models.TextField(null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

class Location(SEO):
    name = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "location"

class ServiceLocation(SEO):
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.service.name} - {self.location.name}'

    class Meta:
        db_table = 'service_locations'

class Service(SEO):
    name = models.TextField()
    locations = models.ManyToManyField(Location, through=ServiceLocation)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "service"

class Lead(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    message = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    date_created = models.DateTimeField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.service.name}"

    class Meta:
        db_table = "lead"

class Marketing(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True)
    landing_page = models.CharField(max_length=255)
    referrer = models.CharField(max_length=100, blank=True, null=True)
    keyword = models.CharField(max_length=100, blank=True, null=True)
    channel = models.CharField(max_length=100, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    medium = models.CharField(max_length=255, blank=True, null=True)
    ad_campaign = models.CharField(max_length=255, blank=True, null=True)
    ad_group = models.CharField(max_length=255, blank=True, null=True)
    ad_headline = models.CharField(max_length=255, blank=True, null=True)
    gclid = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "marketing"