from django.db import models

class Location(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "location"

class ServiceLocation(models.Model):
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.service.name} - {self.location.name}'

    class Meta:
        db_table = 'service_locations'

class Service(models.Model):
    name = models.TextField()
    locations = models.ManyToManyField(Location, through=ServiceLocation)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "service"

class Lead(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True, db_index=True)
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
    landing_page = models.CharField(max_length=45)
    referrer = models.CharField(max_length=255, blank=True, null=True)
    keyword = models.CharField(max_length=45, blank=True, null=True)
    channel = models.CharField(max_length=45, blank=True, null=True)
    source = models.CharField(max_length=45, blank=True, null=True)
    medium = models.CharField(max_length=45, blank=True, null=True)
    ad_campaign = models.CharField(max_length=45, blank=True, null=True)
    ad_group = models.CharField(max_length=45, blank=True, null=True)
    ad_headline = models.CharField(max_length=45, blank=True, null=True)
    gclid = models.CharField(max_length=50, blank=True, null=True)
    language = models.CharField(max_length=15, blank=True, null=True)
    os = models.CharField(max_length=25, blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    button_clicked = models.CharField(max_length=30, blank=True, null=True)
    lead_channel = models.CharField(max_length=15, blank=True, null=True)
    device_type = models.CharField(max_length=15, blank=True, null=True)
    ip = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        db_table = "marketing"