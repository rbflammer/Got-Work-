
from django.db import models
from django.db.models import F
from jobs import models
import requests
import json
import pytz
from datetime import time

from jobs.models import *

# Returns all Pending jobs that match a Worker's preferred type, time, and distance
# This will be the most work of the Job API
# from gotwork.jobs.models import Customer, Worker


def GetWorkerPendingJobs(workerId):
    potentialJobs = Job.objects.filter(status = 'P').order_by("-time")
    worker = Worker.objects.get(pk = workerId)



    outputJobs = []
    for job in potentialJobs:
        if job.time > datetime.now(tz=pytz.timezone('America/Denver')):
            if worker.jobTypes.filter(jobType = job.jobType).exists():
                distanceRequest = requests.get(
                    'https://www.zipcodeapi.com/rest/Bws4w6awN45GFbhUNsOqA9qgKVvlX4JGXJ4CQq4LPipkRZO5trSrXGSTID44PuVj/distance.json/' + str(worker.zipCode) + '/' + str(job.zipCode) + '/mile' 
                    )
                data = distanceRequest.json()
                if data["distance"] <= worker.maximumTravelDistance:
                    addJob = True
                    blacklistedWorkers = job.customer.blacklist.all()
                    for blacklistedWorker in blacklistedWorkers:
                        if blacklistedWorker.id == worker.id:
                            addJob = False
                    if (addJob):
                        outputJobs.append(job)

    if len(worker.availabletimes_set.all()) != 0:
        times = worker.availabletimes_set.all()[0]
        fromTime = times.getFromTime()
        toTime = times.getToTime()
        for job in outputJobs:
            jobTime = job.getDueDate().time()
            if not (fromTime <= jobTime <= toTime):
                outputJobs.remove(job)

    return outputJobs

# Returns all jobs that a Customer has created that do not yet have a worker
def GetCustomerPendingJobs(customerId):
    pendingJobs = Job.objects.filter(customer_id = customerId, status = 'P')
    return pendingJobs

# Returns all Active jobs for a worker
def GetWorkerActiveJobs(workerId):
    UpdateWorkerDueJobs(workerId)
    activeJobs = Job.objects.filter(worker_id = workerId, status = 'A')

    return activeJobs

# Returns all Active jobs for a worker
def GetWorkerActiveAndDueJobs(workerId):
    UpdateWorkerDueJobs(workerId)
    activeJobs = Job.objects.filter(worker_id=workerId, status='A')
    dueJobs = Job.objects.filter(worker_id=workerId, status='D')
    jobs = []
    jobs.extend(activeJobs)
    jobs.extend(dueJobs)
    return jobs

# Returns all Active jobs for a customer
def GetCustomerActiveJobs(customerId):
    UpdateCustomerDueJobs(customerId)
    activeJobs = Job.objects.filter(customer_id = customerId, status = 'A')
    return activeJobs

# Returns all Due jobs for a worker
def GetWorkerDueJobs(workerId):
    UpdateWorkerDueJobs(workerId)
    dueJobs = Job.objects.filter(worker_id = workerId, status = 'D')
    return dueJobs

# Returns all jobs a Worker has finished
def GetWorkerFinishedJobs(workerId):
    finishedJobs = Job.objects.filter(worker_id = workerId, status = 'F')
    return finishedJobs

# Returns all jobs that a Customer has had finished
def GetCustomerFinishedJobs(customerId):
    finishedJobs = Job.objects.filter(customer_id = customerId, status = 'F')
    return finishedJobs

# Returns average completion time of a recurring job
def GetRecurringJobCompletionTime(customerId, job):
    pass

# Connects a worker to a job. Changes the job's status to "Active". 
# Returns a status code True for successful, False for unsuccessful
def AcceptJob(workerId, jobId):
    job = Job.objects.get(id=jobId)
    if not job:
        return False
    job.worker = Worker.objects.get(id=workerId)
    job.status = 'A'
    job.save()
    return True

# Removes a job from the database
# Returns True when successful
def DeleteJob(jobId):
    try:
        Job.objects.get(id=jobId).delete()
        return True
    except:
        return False

# Marks a job as finished. Pays Worker and Owner from Customer
def FinishJob(jobId):
    job = Job.objects.get(id=jobId)
    worker = job.worker
    customer = job.customer
    ownerCount = Owner.objects.all().count()

    price = job.price

    customer.balance -= price
    customer.save()
    worker.balance = worker.balance + (price * 0.9)
    worker.save()
    Owner.objects.all().update(balance=F('balance')+(price * (0.1 / ownerCount))) # Splits 10% amongst all owners

    job.status = 'F'
    job.save()
    pass

# Attaches a rating to a job. Updates a customer's average rating
def RateJob(customerId, jobId, rating):
    customer = Customer.objects.get(id=customerId)
    job = Job.objects.get(id=jobId)

    job.rating = rating

    if rating == True:
        customer.averageRating = ((customer.averageRating * customer.numberOfRatings) + 1) / (customer.numberOfRatings + 1)
        customer.numberOfRatings += 1
    else:
        customer.averageRating = ((customer.averageRating * customer.numberOfRatings) + 0) / (customer.numberOfRatings + 1)
        customer.numberOfRatings += 1
    customer.save()
    pass

# Attaches a completion time to a job. Calls FinishJob if job is not finished
def AddCompletionTime(jobId, completionTime):
    job = Job.objects.get(id=jobId)
    job.completionTime = completionTime
    job.save()

    if job.status != 'F':
        FinishJob(job.id)
    pass

# Intended to be used internally by GetWorkerFinishedJobs, GetWorkerDueJobs, and GetWorkerActiveJobs methods
def UpdateWorkerDueJobs(workerId):
    worker = Worker.objects.get(id=workerId)
    jobs = Job.objects.filter(worker_id = worker.id, status = 'A')

    for job in jobs:
        if datetime.now(tz=pytz.timezone('America/Denver')) > job.time:
            job.status = 'D'
            job.save()
    pass

# Intended to be used internally by GetCustomerFinishedJobs, GetCustomerDueJobs, and GetCustomerActiveJobs methods
def UpdateCustomerDueJobs(customerId):
    customer = Customer.objects.get(id=customerId)
    jobs = Job.objects.filter(customer_id = customer.id, status = 'A')
    
    for job in jobs:
        if datetime.now(tz=pytz.timezone('America/Denver')) > job.time:
            job.status = 'D'
            job.save()            

def GetAllJobTypes():
    return JobType.objects.all()

def UpdateWorkerSettings(worker_id, first_name='First', last_name='Last', email='default@email.com', zipCode=11111, distance=50, jobTypes=[], fromTime="0:00", toTime="23:59"):
    worker = Worker.objects.get(id=worker_id)
    while len(worker.availabletimes_set.all()) != 0:
        worker.availabletimes_set.all()[0].delete()

    splitfrom = fromTime.split(":")
    fromTime = time(int(splitfrom[0]), int(splitfrom[1]), 0)
    splitto = toTime.split(":")
    toTime = time(int(splitto[0]), int(splitto[1]), 0)
    times = AvailableTimes(worker=worker, fromTime=fromTime, toTime=toTime)
    times.save()

    worker.first_name = first_name
    worker.last_name = last_name
    worker.email = email
    worker.zipCode = zipCode
    worker.maximumTravelDistance = distance
    allJobTypes = GetAllJobTypes()
    for type in allJobTypes:
        worker.jobTypes.remove(type)
    for type in jobTypes:
        worker.jobTypes.add(type)
    worker.save()

def UpdateCustomerSettings(customer_id, first_name='First', last_name='Last', email='default@email.com', zipCode=11111, phoneNumber="111-555-1111", defaultAddress="Homeless"):
    customer = Customer.objects.get(id=customer_id)
    customer.first_name = first_name
    customer.last_name = last_name
    customer.email = email
    customer.zipCode = zipCode
    customer.phoneNumber = phoneNumber
    customer.defaultAddress = defaultAddress
    customer.save()

def UpdateCustomerRatings(customer_id, rating_num=0):
    customer = Customer.objects.get(id=customer_id)
    ratingsSum = (customer.averageRating * customer.numberOfRatings) + rating_num
    customer.numberOfRatings += 1
    customer.averageRating = ratingsSum / customer.numberOfRatings
    customer.save()

def UpdateWorkerRatings(worker_id, rating_num=0):
    worker = Worker.objects.get(id=worker_id)
    if (worker.averageRating):
        averageRating = worker.averageRating
    else:
        averageRating = 0.0

    if (worker.numberOfRatings):
        numOfRatings = worker.numberOfRatings
    else:
        numOfRatings = 0
    ratingsSum = (averageRating * numOfRatings) + rating_num
    worker.numberOfRatings += 1
    worker.averageRating = ratingsSum / worker.numberOfRatings
    worker.save()

def UpdateOwnerSettings(owner_id, first_name='First', last_name='Last', email='default@email.com', zipCode=11111):
    owner = Owner.objects.get(id=owner_id)
    owner.first_name = first_name
    owner.last_name = last_name
    owner.email = email
    owner.zipCode = zipCode
    owner.save()


def GetWorkerDisputedJobs(worker_id):
    jobs = Job.objects.filter(worker_id=worker_id, status='I')
    return jobs
    
# Changes a job's status to disputed after a refund request is sent
def DisputeJob(job_id):
    job = Job.objects.get(id=job_id)
    job.status = 'I'
    job.save()

def SetJobAsReviewed(job_id):
    job = Job.objects.get(id=job_id)
    job.status = 'R'
    job.save()

def CreateCustomerAccount(username='user', first_name='First', last_name='Last', email='default@email.com',password="password1",zipCode=11111, balance=0, phone=1234567899, address=("wicked witch of the west house")):
    customer = Customer()
    customer.username =  username
    customer.first_name = first_name
    customer.last_name = last_name
    customer.email = email
    customer.zipCode = zipCode
    customer.set_password(password)
    customer.balance = balance
    customer.accountType="C"
    customer.phoneNumber=phone
    customer.defaultAddress=address
    customer.save()

def CreateWorkerAccount(username='user', first_name='First', last_name='Last', email='defaults@email.com', password="password1", zipCode=11111, distance=50, fromTime="0:00", toTime="23:59"):
    worker = Worker()
    worker.username =  username
    worker.first_name = first_name
    worker.last_name = last_name
    worker.email = email
    worker.set_password(password)
    worker.zipCode = zipCode
    worker.maximumTravelDistance = distance
    splitfrom = fromTime.split(":")
    fromTime = time(int(splitfrom[0]), int(splitfrom[1]), 0)
    splitto = toTime.split(":")
    toTime = time(int(splitto[0]), int(splitto[1]), 0)
    times = AvailableTimes(worker=worker, fromTime=fromTime, toTime=toTime)
    worker.save()
    times.save()

# Refunds the money taken from a job back to Customer
# Takes price of job away from Worker and Owners
def RefundMoney(request_id):
    request = RefundRequest.objects.get(id=request_id)
    job = Job.objects.get(id=request.job.id)
    customer = Customer.objects.get(id=job.customer.id)
    worker = Worker.objects.get(id=job.worker.id)
    ownerCount = Owner.objects.all().count()

    price = job.price

    # Returning money back to customer, taking money back from worker and owners
    customer.balance += price
    customer.save()
    worker.balance = worker.balance - (price * 0.9)
    worker.save()
    Owner.objects.all().update(balance=F('balance')-(price * (0.1 / ownerCount))) # Splits 10% amongst all owners

def CloseRefundRequest(request_id):
    request = RefundRequest.objects.get(id=request_id)
    job = Job.objects.get(id=request.job.id)

    job.status = 'R'
    job.save()

    # TODO: Do we really want to delete refund requests once they're done?
    try:
        RefundRequest.objects.get(id=request_id).delete()
        return True
    except:
        return False

def BlacklistWorker(job_id):
    job = Job.objects.get(id=job_id)
    customer = Customer.objects.get(id=job.customer.id)
    worker = Worker.objects.get(id=job.worker.id)

    customer.blacklist.add(worker)
    customer.save()

