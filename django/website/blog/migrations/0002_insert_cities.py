from django.db import migrations
from django.utils.text import slugify

def insert_cities(apps, schema_editor):
    Location = apps.get_model('blog', 'Location')

    # List of cities
    cities = [
        "Miami",
        "Miami Beach",
        "Hialeah",
        "Coral Gables",
        "Miami Gardens",
        "Homestead",
        "North Miami",
        "Doral",
        "Cutler Bay",
        "Aventura",
        "Palmetto Bay",
        "Miami Springs",
        "Sweetwater",
        "Miami Lakes",
        "South Miami",
        "Opa-locka",
        "Sunny Isles Beach",
        "Key Biscayne",
        "Bal Harbour",
        "Pinecrest",
        "North Miami Beach",
        "West Miami",
        "Virginia Gardens",
        "El Portal",
        "Miami Shores",
        "Medley",
        "Golden Beach",
        "Surfside",
        "Bay Harbor Islands",
        "Indian Creek",
        "Fisher Island",
        "Westchester",
        "Kendall",
        "Tamiami",
        "Fontainebleau",
        "Coral Terrace",
        "Westwood Lakes",
        "Olympia Heights",
        "Glenvar Heights",
        "Richmond Heights",
        "West Little River",
        "Westview",
        "Sunset",
        "Country Walk",
        "Princeton",
        "The Crossings",
        "Kendale Lakes",
        "Kendale Lakes-Lindgren Acres",
        "Three Lakes",
        "The Hammocks",
        "Palmetto Estates",
        "Richmond West",
        "Naranja",
        "Leisure City",
        "Florida City",
        "Brownsville",
        "Liberty City",
        "Little Haiti",
        "Wynwood",
        "Allapattah",
        "Overtown",
        "Coconut Grove",
        "Brickell",
        "Downtown Miami",
        "Edgewater",
        "Midtown Miami",
        "Buena Vista",
        "Upper Eastside",
        "Little Havana",
        "Flagami",
        "West Flagler",
        "Coral Way",
        "Grapeland Heights",
        "Model City",
        "Pinewood",
        "West Perrine",
        "South Miami Heights",
        "Country Club",
        "Fountainbleau",
        "Blue Lagoon",
        "Andover",
        "Scott Lake",
        "Norland",
        "Ives Estates",
        "Lake Lucerne",
        "Palm Springs North",
        "Carol City",
        "Bunche Park",
        "Golden Glades",
        "Miramar",
        "Hialeah Gardens"
    ]

    # Insert cities into the database
    for city in cities:
        slug = slugify(city)
        Location.objects.create(name=city, slug=slug)

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_cities),
    ]
