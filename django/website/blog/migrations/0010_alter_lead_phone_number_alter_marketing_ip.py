# Generated by Django 4.1.7 on 2023-11-23 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_marketing_user_agent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='phone_number',
            field=models.CharField(db_index=True, max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='marketing',
            name='ip',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
    ]
