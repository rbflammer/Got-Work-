# Generated by Django 4.0 on 2022-02-25 02:24
from django.contrib.auth.hashers import make_password
from django.db import migrations
from pkg_resources import AvailableDistributions
#from django.utils import timezone
from datetime import datetime, timezone, time
#import pytz

#from jobs.models import Owner, Job, Customer, Worker, AvailableTimes, JobType
def populate_db(apps, schema_editor):
    Owner = apps.get_model('jobs', 'Owner')
    Job = apps.get_model('jobs', 'Job')
    Customer = apps.get_model('jobs', 'Customer')
    Worker = apps.get_model('jobs', 'Worker')
    AvailableTimes = apps.get_model('jobs', 'AvailableTimes')
    JobType = apps.get_model('jobs', 'JobType')
    RefundRequest = apps.get_model('jobs', 'RefundRequest')


    # Create 3 Job types: Mowing, Blowing, Raking
    
    jobTypeMowing = JobType(jobType="Lawn Mowing")
    jobTypeMowing.save()
    jobTypeBlowing = JobType(jobType="Snow Blowing")
    jobTypeBlowing.save()
    jobTypeRaking = JobType(jobType="Leaf Raking")
    jobTypeRaking.save()

    # Create 3 customers
    customerLogan = Customer(
            password="Logan", email="Logan@whoami.com", 
            username="Logan",   first_name="Logan", 
            last_name="NoLastName", balance=1337,
            zipCode=84321, accountType='C', phoneNumber="621-555-4516", 
            defaultAddress="123 Wizard Way", averageRating=5, numberOfRatings=3
        )
    customerLogan.password=make_password("Logan")
    customerLogan.save()

    customerBoise = Customer(
            password="Boise", email="Boise@hotmail.com", 
            username="Boise",   first_name="Boise", 
            last_name="Winchester", balance=1500.0,
            zipCode=83701, accountType='C', phoneNumber="785-555-0128", 
            defaultAddress="1967 Winchester Avenue", averageRating=4.5, numberOfRatings=576
        )
    customerBoise.password= make_password("Boise")
    customerBoise.save()

    customerManhattan = Customer(
        password="Manhattan", email="Manhattanw@hotmail.com", 
        username="KingOf",   first_name="Manhattan", 
        last_name="Winchester", balance=1500.0,
        zipCode=10001, accountType='C', phoneNumber="777-555-0182", 
        defaultAddress="1967 Winchester Avenue", averageRating=3.0, numberOfRatings=5
    )
    customerManhattan.password= make_password("Manhattan")
    customerManhattan.save()


    # Create 4 workers
    workerBilly = Worker(
            password="billyjoel", email="billy@joel.com",
            username="billyjoel",   first_name="Billy", 
            last_name="Joel", balance=1337.0,
            zipCode=84341, accountType='W', maximumTravelDistance=25        )

    workerBilly.password = make_password("billyjoel")

    workerBilly.save()
    workerBilly.jobTypes.add(jobTypeMowing, jobTypeBlowing)

    workerTommy = Worker(
            password="Tommyboy", email="Tommy@boy.com",
            username="Tommyboy",   first_name="Tommy", 
            last_name="Boy", balance=25.0,
            zipCode=84341, accountType='W', maximumTravelDistance=400
        )

    workerTommy.password = make_password("Tommyboy")

    workerTommy.save()
    workerTommy.jobTypes.add(jobTypeMowing, jobTypeRaking)

    workerSam = Worker(
            password="sammy", email="sammy@hotmail.com", 
            username="sammy",   first_name="Sam", 
            last_name="Winchester", balance=1983.0,
            zipCode=83701, accountType='W', maximumTravelDistance=300
        )
    workerSam.password=make_password("sammy")
    workerSam.save()
    workerSam.jobTypes.add(jobTypeMowing, jobTypeBlowing, jobTypeRaking)

    workerWolf = Worker(
            password="ofwallstreet", email="wolf@wallstreet.com",
            username="wolf",   first_name="Wolf", 
            last_name="of Wall Street", balance=100000.0,
            zipCode=10001, accountType='W', maximumTravelDistance=30
        )

    workerWolf.password = make_password("ofwallstreet")

    workerWolf.save()
    workerWolf.jobTypes.add(jobTypeMowing, jobTypeBlowing, jobTypeRaking)

    # Create 3 available times
    allDay = AvailableTimes(
        worker_id=workerWolf.id,
        fromTime=time(0, 0, 0),
        toTime=time(23, 59, 59),
    )
    allDay.save()

    firstHalf = AvailableTimes(
        worker_id=workerBilly.id,
        fromTime=time(0, 0, 0),
        toTime=time(11, 59, 59),
    )
    firstHalf.save()

    secondHalf = AvailableTimes(
        worker_id=workerSam.id,
        fromTime=time(12, 0, 0),
        toTime=time(23, 59, 59),
    )
    secondHalf.save()

    #Create 6 jobs, link to customers and jobtypes

    jobMowing = Job(
        price=57.0, address="4589 S 4875 N Paris, Idaho", zipCode=83261, 
        time=datetime(2022, 5, 1, 12, 59, 28, 0, timezone.utc), recurring=True,
        rating=False, completionTime=90.0, status='P', customer_id=customerLogan.id,
        jobType_id=jobTypeMowing.id
    )
    jobMowing.save()

    jobRaking = Job(
        price=800.0, address="7459 Gold St.", zipCode=84321, 
        time=datetime(2022, 5, 16, 18, 00, 00, 0, timezone.utc), recurring=False,
        rating=False, completionTime=20.0, status='P', customer_id=customerLogan.id,
        jobType_id=jobTypeRaking.id,
    )
    jobRaking.save()

    jobBlowing = Job(
        price=1337.0, address="That creepy house down the way", zipCode=83709, 
        time=datetime(2022, 5, 26, 16, 30, 21, 0, timezone.utc), recurring=True,
        rating=True, completionTime=-5.5, status='P', customer_id=customerBoise.id,
        jobType_id=jobTypeBlowing.id,
    )
    jobBlowing.save()

    jobActive = Job(
        price=50.0, address="Townhouses By Macey's", zipCode=84332, 
        time=datetime(2022, 3, 26, 16, 30, 21, 0, timezone.utc), recurring=False,
        rating=True, completionTime=-0.5, status='A', customer_id=customerLogan.id,
        worker_id=workerTommy.id, jobType_id=jobTypeBlowing.id,
    )
    jobActive.save()

    jobDisputed = Job(
        price=100000.0, address="1234 Wall Street", zipCode=10001, 
        time=datetime(2022, 3, 30, 8, 30, 21, 0, timezone.utc), recurring=True,
        rating=True, completionTime=-5.5, status='I', customer_id=customerManhattan.id,
        worker_id=workerWolf.id, jobType_id=jobTypeBlowing.id,
    )
    jobDisputed.save()

    jobNewYork = Job(
        price=20.0, address="5678 Wall Street", zipCode=10001, 
        time=datetime(2022, 3, 30, 8, 30, 21, 0, timezone.utc), recurring=True,
        rating=True, completionTime=-1.5, status='P', customer_id=customerManhattan.id,
        jobType_id=jobTypeMowing.id,    
    )
    jobNewYork.save()

    refundRequest = RefundRequest(
        job_id = jobDisputed.id, 
        description="Wolf really took advantage of me, I do not think his work is worth his pay.",
    )
    refundRequest.save()

    # Create an owner

    owner = Owner(
        password="owner", username="owner", email="owner@boss.com", first_name="Awesome", 
        last_name="Owner", balance=0, zipCode=11111, accountType='O'
    )
    owner.password = make_password("owner")
    owner.save()




class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0008_alter_availabletimes_fromtime_and_more'),
    ]

    operations = [
        migrations.RunPython(populate_db)
    ]