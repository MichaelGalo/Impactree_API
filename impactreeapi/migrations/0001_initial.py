# Generated by Django 5.1.2 on 2024-10-17 15:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CharityCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Charity Categories',
            },
        ),
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('required_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('image_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Charity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('impact_metric', models.CharField(max_length=255)),
                ('impact_ratio', models.FloatField()),
                ('website_url', models.URLField()),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='impactreeapi.charitycategory')),
            ],
            options={
                'verbose_name_plural': 'Charities',
            },
        ),
        migrations.CreateModel(
            name='ImpactPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annual_income', models.DecimalField(decimal_places=2, max_digits=12)),
                ('philanthropy_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('total_annual_allocation', models.DecimalField(decimal_places=2, max_digits=12)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('current_milestone', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='impactreeapi.milestone')),
            ],
        ),
        migrations.CreateModel(
            name='ImpactPlanCharity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allocation_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('charity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='impactreeapi.charity')),
                ('impact_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='impactreeapi.impactplan')),
            ],
            options={
                'verbose_name_plural': 'Impact Plan Charities',
            },
        ),
    ]
