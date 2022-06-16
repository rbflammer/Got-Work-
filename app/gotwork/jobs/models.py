from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, zipCode, password=None):
        if not email:
            raise ValueError("Users must have an email")
        if not username:
            raise ValueError("Users must have a username")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")
        if not zipCode:
            raise ValueError("Users must have a zip code")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            zipCode=zipCode
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, username, first_name, last_name, zipCode, password):
        if not email:
            raise ValueError("Users must have an email")
        if not username:
            raise ValueError("Users must have a username")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")
        if not zipCode:
            raise ValueError("Users must have a zip code")

        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            zipCode=zipCode,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self.db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    balance = models.FloatField(default=0.0)
    zipCode = models.IntegerField()

    ACCOUNTTYPES = [
        ('W', 'Worker'),
        ('C', 'Customer'),
        ('O', 'Owner'),
    ]

    accountType = models.CharField(max_length=1, choices=ACCOUNTTYPES, default="W")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'zipCode']

    objects = CustomUserManager()

    def __str__(self):
        return self.get_full_name()

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

    def get_full_name(self):
        return str(self.first_name) + " " + str(self.last_name)

    # class Meta:
    #     abstract = True

class JobType(models.Model):
    jobType = models.TextField()
    def __str__(self):
        return self.jobType

class Worker(CustomUser):    
    jobTypes = models.ManyToManyField(JobType) # Many to Many field used because a worker can set many jobtypes, and a jobtype can be connected to many workers
    maximumTravelDistance = models.IntegerField()
    averageRating = models.FloatField(blank=True, null=True)
    numberOfRatings = models.IntegerField(default=0)

    def sortedAvailableTimes(self):
        return self.availabletimes_set_order_by("-availabletime") # For ascending order, remove '-'
    def sortedAcceptedJobs(self):
        return self.job_set_order_by("-time")

class AvailableTimes(models.Model):  #Used to store the available times of a worker. 
    worker = models.ForeignKey(Worker, on_delete = models.CASCADE)
    fromTime = models.TimeField()
    toTime = models.TimeField()

    def getFromTimeStr(self):
        return self.fromTime.strftime("%H:%M")
    def getToTimeStr(self):
        return self.toTime.strftime("%H:%M")
    def getFromTime(self):
        return self.fromTime
    def getToTime(self):
        return self.toTime
    def __str__(self):
        return self.fromTime.strftime("%H:%M:%S") + " to " +  self.toTime.strftime("%H:%M:%S")

class Customer(CustomUser):
    def sortedJobs(self):
        return self.job_set_order_by("-time")
    phoneNumber = models.TextField()
    defaultAddress = models.TextField(blank=True, null=True)
    averageRating = models.FloatField(blank=True, null=True)
    numberOfRatings = models.IntegerField(default=0)
    blacklist = models.ManyToManyField(Worker, blank=True)

class Owner(CustomUser):
    # Empty
    pass

class Job(models.Model):
    worker = models.ForeignKey(Worker, on_delete = models.SET_NULL, null=True, blank=True)  # Connects the job to a worker. If the worker is deleted, then the job is not.
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)  # If the customer is deleted, then the job is deleted
    
    price = models.FloatField()
    address = models.TextField()
    zipCode = models.IntegerField()
    time = models.DateTimeField()
    recurring = models.BooleanField()
    rating = models.BooleanField(blank=True, null=True)
    completionTime = models.FloatField(blank=True, null=True)

    refunddescription = models.TextField(blank=True, null=True)
    
# TODO: Should the job be deleted if its job type is removed?
    jobType = models.ForeignKey(JobType, on_delete = models.CASCADE) # ForeignKey used because each job will only have one type. If the jobtype is deleted, then the job will be deleted
    
    STATUSSTATES = [
        ('P', 'Pending'),
        ('A', 'Active'),
        ('D', 'Due'), # This is for a job that is past it's completion time, but not marked completed
        ('I', 'Disputed'), # For jobs with a refund request pending
        ('F', 'Finished'),
        ('R', 'Reviewed'), # For jobs that have been completely closed, no refund request or extra reviews pending
    ]
    
    status = models.CharField(max_length=1, choices=STATUSSTATES, default='P')

    def getDueDate(self):
        return self.time

    def getDueDatePretty(self):
        return self.time.strftime("%m/%d/%Y, %I:%M %p")

    def __str__(self):
        return "Job for " + self.jobType.__str__() + " on " + self.time.strftime("%m/%d/%Y, %H:%M:%S")

class RefundRequest(models.Model):
    job = models.ForeignKey(Job, on_delete = models.CASCADE)
    description = models.TextField()
    def __str__(self):
        return self.description 