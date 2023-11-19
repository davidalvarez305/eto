from django.db import migrations
from django.utils.text import slugify

def insert_service_locations(apps, schema_editor):
    Service = apps.get_model('blog', 'Service')
    services = Service.objects.all()

    Location = apps.get_model('blog', 'Location')
    locations = Location.objects.all()

    ServiceLocation = apps.get_model('blog', 'ServiceLocation')

    for service in services:
        for location in locations:
            slug = slugify(f'{service.slug} {location.slug}')
            service_id = service.id
            location_id = location.id
            ServiceLocation.objects.create(location_id=location_id, service_id=service_id, slug=slug)

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_servicelocation_create'),
    ]

    operations = [
        migrations.RunPython(insert_service_locations),
    ]
