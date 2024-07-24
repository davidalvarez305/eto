# Generated by Django 4.1.7 on 2024-07-22 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_alter_marketing_gclid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='marketing',
            name='device_type',
        ),
        migrations.RemoveField(
            model_name='marketing',
            name='os',
        ),
        migrations.AddField(
            model_name='lead',
            name='bathrooms',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='is_house',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='pets',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='square_feet',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='total_rooms',
            field=models.IntegerField(null=True),
        ),
    ]