# Generated by Django 4.1.7 on 2023-12-25 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_alter_lead_first_name_alter_lead_last_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketing',
            name='gclid',
            field=models.TextField(blank=True, null=True, unique=True),
        ),
    ]
