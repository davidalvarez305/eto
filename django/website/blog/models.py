from django.db import models

class SEO(models.Model):
    title = models.CharField(max_length=255)
    meta_description = models.TextField()
    slug = models.SlugField(db_index=True, unique=True)
    content = models.TextField()

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

class Service(SEO):
    name = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "service"

class Lead(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    date_created = models.DateTimeField()

class Marketing(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL)
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