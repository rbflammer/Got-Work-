# Generated by Django 3.2.8 on 2022-03-15 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_auto_20220315_1338'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='refunddescription',
            field=models.TextField(blank=True),
        ),
    ]
