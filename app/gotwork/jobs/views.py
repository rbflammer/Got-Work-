from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from json import dumps
from jobs.utility import *
from django.contrib.auth import get_user_model
import logging

from jobs.models import Job, Worker, Customer, Owner



def frontPage(request):
    return render(request, 'jobs/front_page.html')

def genericSignUp(request):
    return render(request, 'jobs/generic_sign_up.html')


def workerSignUp(request):
    return render(request, 'jobs/worker_sign_up.html')

def customerSignUp(request):
    return render(request, 'jobs/customer_sign_up.html')

def userHome(request):
    if not request.user.is_authenticated:
        return render(request, 'jobs/login_error.html')
    user = CustomUser.objects.get(id=request.user.id)
    if user.accountType == 'W':
        return HttpResponseRedirect(reverse('jobs:workerHome'))
    elif user.accountType == 'C':
        return HttpResponseRedirect(reverse('jobs:customerHome'))
    elif user.accountType == 'O':
        return HttpResponseRedirect(reverse('jobs:ownerHome', args=(" ")))
    else:
        return HttpResponseRedirect(reverse('jobs:frontPage'))



def workerHome(request):
    if not request.user.is_authenticated or request.user.accountType != 'W':
        return render(request, 'jobs/login_error.html')
    print(request.user.accountType)
    worker = Worker.objects.get(id=request.user.id)

    available_jobs = GetWorkerPendingJobs(request.user.id)
    active_jobs = GetWorkerActiveAndDueJobs(request.user.id)
    disputed_jobs = GetWorkerDisputedJobs(request.user.id)
    context = {
        'available_jobs' : available_jobs,
        'worker' : worker,
        'active_jobs' : active_jobs,
        'disputed_jobs' : disputed_jobs,
    }
    return render(request, 'jobs/worker_home.html', context)

def customerHome(request):
    if not request.user.is_authenticated or request.user.accountType != 'C':
        return render(request, 'jobs/login_error.html')
    customer = Customer.objects.get(id=request.user.id)
    active_jobs = GetCustomerActiveJobs(request.user.id)
    pending_jobs = GetCustomerPendingJobs(request.user.id)
    finished_jobs = GetCustomerFinishedJobs(request.user.id)
    
    context = {
        'customer' : customer,
        'active_jobs' : active_jobs,
        'pending_jobs' : pending_jobs,
        'finished_jobs' : finished_jobs,
    }

    return render(request, 'jobs/customer_home.html', context)

def ownerHome(request, message=" "):
    if not request.user.is_authenticated or request.user.accountType != 'O':
        return render(request, 'jobs/login_error.html')
    owner = Owner.objects.get(id=request.user.id)
    # TODO: How do we want to handle refund requests?
    refund_requests = RefundRequest.objects.all()

    context = {
        'owner' : owner,
        'refund_requests' : refund_requests,
        'message' : message,
    }

    return render(request, 'jobs/owner_home.html', context)

def acceptJob(request, job_id, worker_id):
    job = get_object_or_404(Job, pk=job_id)
    worker = get_object_or_404(Worker, pk=worker_id)
    print("worker " + str(worker_id) + " accepted job " + str(job_id))
    AcceptJob(worker_id, job_id)
    #send back to worker home
    return HttpResponseRedirect(reverse('jobs:workerHome'))

def finishJob(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    customer = job.customer
    worker = job.worker
    completionTime = request.POST["timetaken"]
    print("worker" + str(worker.id) + " finished job " + str(job_id))
    FinishJob(job_id) #customer parameter?
    AddCompletionTime(job_id, completionTime)
    # Update the customer's ratings
    rating = request.POST["review"]
    # If thumbs up then rating is 10, if thumbs down then rating is 0
    ratingNum = 0
    if (rating == "up"):
        ratingNum = 10
    UpdateCustomerRatings(customer.id, ratingNum)
    # Send back to worker home
    return HttpResponseRedirect(reverse('jobs:workerHome'))

def reviewWorker(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    customer = job.customer
    worker = job.worker
    # Update the worker's ratings
    rating = request.POST["review"]
    # If thumbs up then rating is 10, if thumbs down then rating is 0
    ratingNum = 0
    if (rating == "up"):
        ratingNum = 10
    UpdateWorkerRatings(worker.id, ratingNum)

    # If the user requested a refund, create a refund request
    try:
        reason = request.POST["reason"]
        if (reason and reason.strip()):
            refundRequest = RefundRequest.objects.create(job=job, description=reason)
            refundRequest.save()
            DisputeJob(job_id)
        else:
            SetJobAsReviewed(job_id)
    except:
        SetJobAsReviewed(job_id)

    # See if the user chose to blacklist the worker
    try:
        blacklist = request.POST["blacklist"]
        if (blacklist):
            print("Customer " + str(customer.id) + " blacklisted " + str(worker.id))
            BlacklistWorker(job_id)
    except:
        # Do nothing
        print()

    # Send back to customer home
    return HttpResponseRedirect(reverse('jobs:customerHome'))

def deleteJob(request, job_id):
    job = Job.objects.get(pk=job_id)
    job.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  #  Redirects to previous page

def workerSettings(request, worker_id):
    user = get_object_or_404(Worker, pk=worker_id)
    job_types = GetAllJobTypes()
    fromTime = "07:00" #some default data to display
    toTime = "19:00" #some default data to display
    if len(user.availabletimes_set.all()) != 0:
        fromTime = str(user.availabletimes_set.all()[0].getFromTimeStr())
        toTime = str(user.availabletimes_set.all()[0].getToTimeStr())

    context = {
        'user' : user,
        'fromTime' : fromTime,
        'toTime' : toTime,
        'job_types' : job_types,
    }
    return render(request, 'jobs/worker_settings.html', context)

def customerSettings(request, customer_id):
    user = get_object_or_404(Customer, pk=customer_id)
    context = {
        'user' : user,
    }
    return render(request, 'jobs/customer_settings.html', context)

def ownerSettings(request, owner_id):
    user = get_object_or_404(Owner, pk=owner_id)
    context = {
        'user' : user,
    }
    return render(request, 'jobs/owner_settings.html', context)

def approveDenyRequest(request, request_id, owner_id):
    refundRequest = get_object_or_404(RefundRequest, pk=request_id)
    requestReview = request.POST.get("finished")

    owner = Owner.objects.get(id=owner_id)
    job = Job.objects.get(id=refundRequest.job.id)
    if (owner.balance < job.price / 10):
        print("Refund request cannot be accepted: insuficient funds")
        return HttpResponseRedirect(reverse('jobs:ownerHome', args=["Refund request cannot be accepted due to insufficient funds."]))
    else:

        # Refund money if request was accepted
        if (requestReview == "Accept"):
            RefundMoney(refundRequest.id)
        CloseRefundRequest(refundRequest.id)
        
        return HttpResponseRedirect(reverse('jobs:ownerHome', args=(" ")))

def postWorkerSettings(request, worker_id):
    worker = Worker.objects.get(pk=worker_id)
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    email = request.POST["email"]
    zipCode = request.POST["zip"]
    distance = request.POST["distance"]
    fromTime = request.POST["starttime"]
    toTime = request.POST["endtime"]

    jobTypes = []
    for jobType in JobType.objects.all():
        if request.POST.get(jobType.jobType, '') == 'on':
            jobTypes.append(jobType)

    UpdateWorkerSettings(worker.id, first_name, last_name, email, zipCode, distance, jobTypes, fromTime, toTime)

    return HttpResponseRedirect(reverse('jobs:workerHome'))

def postCustomerSettings(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    email = request.POST["email"]
    zipCode = request.POST["zip"]
    phoneNumber = request.POST["phone"]
    defaultAddress = request.POST["address"]

    UpdateCustomerSettings(customer.id, first_name, last_name, email, zipCode, phoneNumber, defaultAddress)

    return HttpResponseRedirect(reverse('jobs:customerHome'))


def postOwnerSettings(request, owner_id):
    owner = Owner.objects.get(pk=owner_id)
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    email = request.POST["email"]
    zipCode = request.POST["zip"]

    UpdateOwnerSettings(owner.id, first_name, last_name, email, zipCode)

    return HttpResponseRedirect(reverse('jobs:ownerHome', args=(" ")))


#use utility? CustomUser needs to be abstract, it's causing problems that it has a place in the table.
def depositWorker(request, user_id):
    user = Worker.objects.get(id=user_id)
    amount = request.POST["amount"]
    try:
        user.balance += float(amount)
        user.save()
    except:
        print("amount provided could not be converted to a float")
    return HttpResponseRedirect(reverse('jobs:workerHome'))

def withdrawWorker(request, user_id):
    user = Worker.objects.get(id=user_id)
    amount = request.POST["amount"]
    try:
        if (user.balance - float(amount) >= 0.0):
            user.balance -= float(amount)
            user.save()
        else:
            print("cannot withdraw more than the amount avaialble")
            user.balance = 0
    except:
        print("amount provided could not be converted to a float")
    return HttpResponseRedirect(reverse('jobs:workerHome'))

def depositCustomer(request, user_id):
    user = Customer.objects.get(id=user_id)
    amount = request.POST["amount"]
    try:
        user.balance += float(amount)
        user.save()
    except:
        print("amount provided could not be converted to a float")
    return HttpResponseRedirect(reverse('jobs:customerHome'))

def withdrawCustomer(request, user_id):
    user = Customer.objects.get(id=user_id)
    amount = request.POST["amount"]
    try:
        if (user.balance - float(amount) >= 0.0):
            user.balance -= float(amount)
            user.save()
        else:
            print("cannot withdraw more than the amount avaialble")
            user.balance = 0
    except:
        print("amount provided could not be converted to a float")
    return HttpResponseRedirect(reverse('jobs:customerHome'))

def depositOwner(request, user_id):
    user = Owner.objects.get(id=user_id)
    amount = request.POST["amount"]
    try:
        user.balance += float(amount)
        user.save()
    except:
        print("amount provided could not be converted to a float")
    return HttpResponseRedirect(reverse('jobs:ownerHome', args=(" ")))

def withdrawOwner(request, user_id):
    user = Owner.objects.get(id=user_id)
    amount = request.POST["amount"]
    try:
        if (user.balance - float(amount) >= 0.0):
            user.balance -= float(amount)
            user.save()
        else:
            print("cannot withdraw more than the amount avaialble")
            user.balance = 0
    except:
        print("amount provided could not be converted to a float")
    return HttpResponseRedirect(reverse('jobs:ownerHome', args=(" ")))

def utilityTestWorker(request, worker_id):
    # jobs = Job.objects.order_by('-time')
    
    #TODO remove active jobs from this list.
    
    worker = get_object_or_404(Worker, pk=worker_id); # to be filled in once models are created
    jobs = GetWorkerPendingJobs(worker_id)
    active_jobs = GetWorkerActiveJobs(worker_id).order_by('-time')
    # active_jobs = worker.job_set.order_by('-time')
    context = {
        'jobs' : jobs,
        'worker' : worker,
        'active_jobs' : active_jobs,
    }
    return render(request, 'jobs/utility_test_worker.html', context)

def utilityTestCustomer(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    jobs = customer.job_set.order_by('-time')
    active_jobs = jobs
    pending_jobs = []
    
    context = {
        'customer' : customer,
        'active_jobs' : active_jobs,
        'pending_jobs' : pending_jobs,
    }

    return render(request, 'jobs/utility_test_customer.html', context)

def createJob(request, customer_id, error=""):
    customer = get_object_or_404(Customer, pk=customer_id)
    jobTypes = JobType.objects.all()
    context = {
        'customer' : customer,
        'jobTypes' : jobTypes,
        'error' : error,
    }
    return render(request, 'jobs/create_job.html', context)
    
def saveJob(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    job = Job()

    job.customer = customer
    job.price = request.POST.get('price', False)
    if not job.price or float(job.price) < 0.01:
        return HttpResponseRedirect(reverse('jobs:createJob', args=(customer.id, "Enter a valid price ($0.01 and up).")))
    job.address = request.POST.get('address', False)
    if not job.address:
        return HttpResponseRedirect(reverse('jobs:createJob', args=(customer.id, "Enter an address.")))
    job.zipCode = request.POST.get('zipCode', False)
    if not job.zipCode:
        return HttpResponseRedirect(reverse('jobs:createJob', args=(customer.id, "Enter a zip code.")))
    job.time = request.POST.get('time',False)
    if not job.time:
        return HttpResponseRedirect(reverse('jobs:createJob', args=(customer.id, "Enter a date and time.")))
    job.recurring = request.POST.get('recurring', False)
    
    job.jobType = JobType.objects.get(jobType = request.POST['type'])
    job.status = 'P'
    job.save()
    return HttpResponseRedirect(reverse('jobs:customerHome'))

def createJobType(request, owner_id, error=""):
    context = {
        'owner_id' : owner_id,
        'error' : error,
    }
    return render(request, 'jobs/create_job_type.html', context)

def saveJobType(request, owner_id):
    newJobType = JobType()

    jobType = request.POST.get('type', False)
    if not jobType:
        return HttpResponseRedirect(reverse('jobs:createJobType', args=(owner_id, "Enter a Job Type")))
    if JobType.objects.filter(jobType=jobType).exists():
        return HttpResponseRedirect(reverse('jobs:createJobType', args=(owner_id, "That Job Type already exists.")))
    newJobType.jobType = jobType
    newJobType.save()

    return HttpResponseRedirect(reverse('jobs:ownerHome', args=(" ")))

def postCustomer(request):
    print(request.body)
    print((request.POST.get("user")))
    first_name = request.POST.get("first_name", "")
    last_name = request.POST.get("last_name", "")
    email =request.POST.get("mail", "")
    zipCode =request.POST.get("zip","")
    if request.POST.get("balance", 0)!="":
        balance= request.POST.get("balance", 0)
    else:
        balance=0
    username=request.POST.get("user", "")
    password=request.POST.get("password", "")
    address=request.POST.get("address", "")
    phone=request.POST.get("phone", "")

    CreateCustomerAccount(username, first_name, last_name, email, password, zipCode, balance, phone, address)
    return HttpResponseRedirect(reverse("jobs:frontPage"))

def createWorker(request):
    first_name = request.POST.get("first_name", "")
    last_name = request.POST.get("last_name", "")
    email =request.POST.get("mail", "")
    zipCode =request.POST.get("zip", 11111)
    distance= request.POST.get("distance", 111111)
    username=request.POST.get("user", "")
    password = request.POST.get("password", "")
    fromTime = request.POST["starttime"]
    toTime = request.POST["endtime"]

    CreateWorkerAccount(username, first_name, last_name, email, password, zipCode, distance, fromTime, toTime)
    return HttpResponseRedirect(reverse("jobs:frontPage"))

def logIn(request):
    logout(request)
    user=authenticate(request, username=request.POST['username'], password=request.POST['password'])

    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("jobs:userHome"))
    else:
        print("that went poorly")
        return HttpResponseRedirect(reverse("jobs:frontPage"))

def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("jobs:frontPage"))