# Generated by Django 4.1.7 on 2023-11-23 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_alter_lead_phone_number_alter_marketing_ip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketing',
            name='button_clicked',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
