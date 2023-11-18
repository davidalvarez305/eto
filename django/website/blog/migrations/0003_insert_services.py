from django.db import migrations
from django.utils.text import slugify

def insert_cities(apps, schema_editor):
    Service = apps.get_model('blog', 'Service')

    # List of cities
    services = [
        "kitchen cleaning",
        "bathroom cleaning",
        "house cleaning",
        "roof cleaning",
        "apartment cleaning",
        "driveway cleaning",
        "gutter cleaning",
        "air ducts cleaning",
        "rug cleaning",
        "ductwork cleaning",
        "window cleaning",
        "vent cleaning",
        "dryer vent cleaning",
        "concrete cleaning",
        "carpet cleaning",
        "upholstery cleaning",
        "grove cleaning",
        "sidewalk cleaning",
        "floor cleaning",
        "power washing",
        "pressure washing",
        "power cleaning",
        "pressure cleaning",
        "residential cleaning",
        "commercial cleaning",
        "office cleaning",
    ]

    # Insert cities into the database
    for service_name in services:
        slug = slugify(service_name)
        Service.objects.create(name=service_name.title(), slug=slug)

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_insert_cities'),
    ]

    operations = [
        migrations.RunPython(insert_cities),
    ]
