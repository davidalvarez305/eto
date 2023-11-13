from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15)),
                ('message', models.TextField()),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
                ('date_created', models.DateTimeField()),
            ],
            options={
                'db_table': 'lead',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True)),
                ('meta_description', models.TextField(null=True)),
                ('slug', models.SlugField(unique=True)),
                ('content', models.TextField(null=True)),
                ('name', models.TextField()),
            ],
            options={
                'db_table': 'location',
            },
        ),
        migrations.CreateModel(
            name='Marketing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('landing_page', models.CharField(max_length=255)),
                ('referrer', models.CharField(blank=True, max_length=100, null=True)),
                ('keyword', models.CharField(blank=True, max_length=100, null=True)),
                ('channel', models.CharField(blank=True, max_length=100, null=True)),
                ('source', models.CharField(blank=True, max_length=255, null=True)),
                ('medium', models.CharField(blank=True, max_length=255, null=True)),
                ('ad_campaign', models.CharField(blank=True, max_length=255, null=True)),
                ('ad_group', models.CharField(blank=True, max_length=255, null=True)),
                ('ad_headline', models.CharField(blank=True, max_length=255, null=True)),
                ('gclid', models.CharField(blank=True, max_length=255, null=True)),
                ('lead', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.lead')),
            ],
            options={
                'db_table': 'marketing',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True)),
                ('meta_description', models.TextField(null=True)),
                ('slug', models.SlugField(unique=True)),
                ('content', models.TextField(null=True)),
                ('name', models.TextField()),
                ('locations', models.ManyToManyField(to='blog.location')),
            ],
            options={
                'db_table': 'service',
            },
        ),
        migrations.AddField(
            model_name='lead',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.location'),
        ),
        migrations.AddField(
            model_name='lead',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.service'),
        ),
    ]
