# Generated by Django 3.2.8 on 2022-03-18 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_job_refunddescription'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='averageRating',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='worker',
            name='numberOfRatings',
            field=models.IntegerField(default=0),
        ),
    ]