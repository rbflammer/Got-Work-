# Generated by Django 4.0 on 2022-02-25 00:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('balance', models.FloatField(default=0.0)),
                ('zipCode', models.IntegerField()),
                ('accountType', models.CharField(choices=[('W', 'Worker'), ('C', 'Customer'), ('O', 'Owner')], default='W', max_length=1)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JobType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobType', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='jobs.customuser')),
                ('phoneNumber', models.TextField()),
                ('defaultAddress', models.TextField(blank=True, null=True)),
                ('averageRating', models.FloatField(blank=True, null=True)),
                ('numberOfRatings', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
            bases=('jobs.customuser',),
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='jobs.customuser')),
            ],
            options={
                'abstract': False,
            },
            bases=('jobs.customuser',),
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='jobs.customuser')),
                ('maximumTravelDistance', models.IntegerField()),
                ('jobTypes', models.ManyToManyField(to='jobs.JobType')),
            ],
            options={
                'abstract': False,
            },
            bases=('jobs.customuser',),
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('address', models.TextField()),
                ('zipCode', models.IntegerField()),
                ('time', models.DateTimeField()),
                ('recurring', models.BooleanField()),
                ('rating', models.BooleanField(blank=True)),
                ('completionTime', models.FloatField(blank=True)),
                ('status', models.CharField(choices=[('P', 'Pending'), ('A', 'Active'), ('D', 'Due'), ('F', 'Finished')], default='P', max_length=1)),
                ('jobType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.jobtype')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.customer')),
                ('worker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jobs.worker')),
            ],
        ),
        migrations.CreateModel(
            name='AvailableTimes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fromTime', models.DateTimeField()),
                ('toTime', models.DateTimeField()),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.worker')),
            ],
        ),
    ]
