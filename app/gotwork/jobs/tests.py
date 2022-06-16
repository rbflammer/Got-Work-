from django.test import TestCase
from jobs.models import *
from django.contrib.auth.hashers import make_password
from datetime import datetime, timezone, time
from jobs.utility import *

# Create your tests here.

class UtilityTest(TestCase):
    def setUp(self):
        jobTypeMowing = JobType(jobType="Lawn Mowing")
        jobTypeMowing.save()
        jobTypeBlowing = JobType(jobType="Snow Blowing")
        jobTypeBlowing.save()
        jobTypeRaking = JobType(jobType="Leaf Raking")
        jobTypeRaking.save()

        # Create 3 customers
        customerLogan = Customer(
                password="Logan", email="mrLogan@whoami.com", 
                username="mrLogan",   first_name="Logan", 
                last_name="NoLastName", balance=1337,
                zipCode=84321, accountType='C', phoneNumber="621-555-4516", 
                defaultAddress="123 Wizard Way", averageRating=1, numberOfRatings=3
            )
        customerLogan.password=make_password("Logan")
        customerLogan.save()

        customerBoise = Customer(
                password="Boise", email="mrBoise@hotmail.com", 
                username="mrBoise",   first_name="Boise", 
                last_name="Winchester", balance=1500.0,
                zipCode=83701, accountType='C', phoneNumber="785-555-0128", 
                defaultAddress="1967 Winchester Avenue", averageRating=4.5, numberOfRatings=576
            )
        customerBoise.password= make_password("Boise")
        customerBoise.save()

        customerManhattan = Customer(
            password="Manhattan", email="mrManhattan@hotmail.com", 
            username="mrKingOf",   first_name="Manhattan", 
            last_name="Winchester", balance=1500.0,
            zipCode=10001, accountType='C', phoneNumber="777-555-0182", 
            defaultAddress="1967 Winchester Avenue", averageRating=3.0, numberOfRatings=5
        )
        customerManhattan.password= make_password("Manhattan")
        customerManhattan.save()


        # Create 4 workers
        workerBilly = Worker(
                password="billyjoel", email="mrbilly@joel.com",
                username="mrbillyjoel",   first_name="Billy", 
                last_name="Joel", balance=1337.0,
                zipCode=84341, accountType='W', maximumTravelDistance=25        )

        workerBilly.password = make_password("billyjoel")

        workerBilly.save()
        workerBilly.jobTypes.add(jobTypeMowing, jobTypeBlowing)

        workerTommy = Worker(
                password="Tommyboy", email="mrTommy@boy.com",
                username="mrTommyboy",   first_name="Tommy", 
                last_name="Boy", balance=25.0,
                zipCode=84341, accountType='W', maximumTravelDistance=400
            )

        workerTommy.password = make_password("Tommyboy")

        workerTommy.save()
        workerTommy.jobTypes.add(jobTypeMowing, jobTypeRaking)

        workerSam = Worker(
                password="sammy", email="mrsammy@hotmail.com", 
                username="mrsammy",   first_name="Sam", 
                last_name="Winchester", balance=1983.0,
                zipCode=83701, accountType='W', maximumTravelDistance=300
            )
        workerSam.password=make_password("sammy")
        workerSam.save()
        workerSam.jobTypes.add(jobTypeMowing, jobTypeBlowing, jobTypeRaking)

        workerWolf = Worker(
                password="ofwallstreet", email="mrwolf@wallstreet.com",
                username="mrwolf",   first_name="Wolf", 
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
            price=57.0, address="Testing 4589 S 4875 N Paris, Idaho", zipCode=83261, 
            time=datetime(2022, 5, 1, 12, 59, 28, 0, timezone.utc), recurring=True,
            rating=False, completionTime=90.0, status='P', customer_id=customerLogan.id,
            jobType_id=jobTypeMowing.id
        )
        jobMowing.save()

        jobRaking = Job(
            price=800.0, address="Testing 7459 Gold St.", zipCode=84321, 
            time=datetime(2020, 5, 16, 18, 00, 00, 0, timezone.utc), recurring=False,
            rating=False, completionTime=20.0, status='A', customer_id=customerLogan.id,
            jobType_id=jobTypeRaking.id, worker_id=workerSam.id
        )
        jobRaking.save()

        jobBlowing = Job(
            price=1337.0, address="Testing That creepy house down the way", zipCode=83709, 
            time=datetime(2020, 5, 26, 16, 30, 21, 0, timezone.utc), recurring=True,
            rating=True, completionTime=-5.5, status='A', customer_id=customerBoise.id,
            jobType_id=jobTypeBlowing.id, worker_id=workerBilly.id,
        )
        jobBlowing.save()

        jobActive = Job(
            price=50.0, address="Testing Townhouses By Macey's", zipCode=84332, 
            time=datetime(2022, 3, 26, 16, 30, 21, 0, timezone.utc), recurring=False,
            rating=True, completionTime=-0.5, status='A', customer_id=customerLogan.id,
            worker_id=workerTommy.id, jobType_id=jobTypeBlowing.id,
        )
        jobActive.save()

        jobDisputed = Job(
            price=1000.0, address="Testing 1234 Wall Street", zipCode=10001, 
            time=datetime(2022, 3, 30, 8, 30, 21, 0, timezone.utc), recurring=True,
            rating=True, completionTime=-5.5, status='I', customer_id=customerManhattan.id,
            worker_id=workerWolf.id, jobType_id=jobTypeBlowing.id,
        )
        jobDisputed.save()

        jobNewYork = Job(
            price=21.0, address="5678 Wall Street", zipCode=10001, 
            time=datetime(2022, 3, 30, 8, 30, 21, 0, timezone.utc), recurring=True,
            rating=True, completionTime=-1.5, status='P', customer_id=customerManhattan.id,
            jobType_id=jobTypeMowing.id,    
        )
        jobNewYork.save()

        refundRequest = RefundRequest(
            job_id = jobDisputed.id, 
            description="Testing Wolf really took advantage of me, I do not think his work is worth his pay.",
        )
        refundRequest.save()

        jobNewYork = Job(
            price=21.1, address="Finished Job", zipCode=10001, 
            time=datetime(2022, 3, 30, 8, 30, 21, 0, timezone.utc), recurring=True,
            rating=True, completionTime=-1.5, status='F', customer_id=customerManhattan.id,
            worker_id=workerWolf.id, jobType_id=jobTypeMowing.id,    
        )
        jobNewYork.save()

        jobNewYork2 = Job(
            price=21.2, address="Testing Finished Job 2", zipCode=10001, 
            time=datetime(2022, 3, 30, 8, 30, 21, 0, timezone.utc), recurring=True,
            rating=True, completionTime=-1.5, status='F', customer_id=customerManhattan.id,
            worker_id=workerBilly.id, jobType_id=jobTypeMowing.id,    
        )
        jobNewYork2.save()

        # Create an owner

        owner = Owner(
            password="owner", username="mrowner", email="mrowner@boss.com", first_name="Awesome", 
            last_name="Owner", balance=1000, zipCode=12345, accountType='O'
        )
        owner.password = make_password("owner")
        owner.save()

        #Create dummy customer with only one job
        dummyCustomer = Customer(
            password="dum", email="dum@dumdum.com", 
            username="dum",   first_name="dum", 
            last_name="Winchester", balance=1400.0,
            zipCode=99501, accountType='C', phoneNumber="777-555-0182", 
            defaultAddress="1967 Winchester Avenue", averageRating=3.0, numberOfRatings=5
        )
        dummyCustomer.save()

        #Create a new job to be deleted by the deletion test
        deleteMe = Job(
            price=75.0, address="Anchorage, Alaska", zipCode=99501, 
            time=datetime(2027, 7, 30, 8, 30, 21, 0, timezone.utc), recurring=True,
            rating=True, completionTime=1.5, status='P', customer_id=dummyCustomer.id,
            jobType_id=jobTypeMowing.id,    
        )
        deleteMe.save()

        activeJob = Job(
            price=75.0, address="Anchorage, Alaska", zipCode=99501, 
            time=datetime(2027, 7, 30, 8, 30, 21, 0, timezone.utc), recurring=True,
            rating=True, completionTime=1.5, status='A', customer_id=customerLogan.id,
            jobType_id=jobTypeMowing.id, worker_id=workerSam.id, 
        )
        activeJob.save()

    def test_update_worker_due_jobs(self):
        worker = Worker.objects.get(username="mrbillyjoel")
        job = Job.objects.get(address="Testing That creepy house down the way")

        # self.assertEqual(job.time < datetime.now(tz=pytz.timezone('America/Denver')), True)
        # self.assertEqual(job.worker.id, worker.id)
        self.assertEqual(job.status, 'A')
        UpdateWorkerDueJobs(worker.id)
        job = Job.objects.get(address="Testing That creepy house down the way")

        job = Job.objects.get(address="Testing That creepy house down the way")
        self.assertEqual(job.status, 'D')
        pass

    def test_update_customer_due_jobs(self):
        customer = Customer.objects.get(username="mrLogan")
        job = Job.objects.get(address="Testing 7459 Gold St.")

        # self.assertEqual(job.time < datetime.now(tz=pytz.timezone('America/Denver')), True)
        # self.assertEqual(job.customer.id, customer.id)
        self.assertEqual(job.status, 'A')
        UpdateCustomerDueJobs(customer.id)
        job = Job.objects.get(address="Testing 7459 Gold St.")

        job = Job.objects.get(address="Testing 7459 Gold St.")
        self.assertEqual(job.status, 'D')
        pass

    def test_get_worker_pending_jobs(self):
        # worker = Worker.objects.get(username="mrTommyboy")
        # result = GetWorkerPendingJobs(worker.id)
        # self.assertEqual(len(result), 2)
        # self.assertEqual(result[1].price, 57.0)
        # self.assertEqual(result[0].price, 800.0)

        worker = Worker.objects.get(username="mrbillyjoel")
        result = GetWorkerPendingJobs(worker.id)

        self.assertEqual(len(result), 0)

        pass

    def test_get_customer_pending_jobs(self):
        customer = Customer.objects.get(username="mrLogan")
        result = GetCustomerPendingJobs(customer.id)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].price, 57.0)
        # self.assertEqual(result[1].price, 800.0)

        customer = Customer.objects.get(username="mrBoise")
        result = GetCustomerPendingJobs(customer.id)
        self.assertEqual(len(result), 0)
        # self.assertEqual(result[0].price, 1337.0)
        
        pass

    def get_worker_active_jobs(self):
        worker = Worker.objects.get(username="mrsammy") # should have 0 jobs
        result = GetWorkerActiveJobs(worker.id)
        self.assertEqual(len(result), 0)


        worker = Worker.objects.get(username="mrwolf") #should have 0 jobs
        result = GetWorkerActiveJobs(worker.id)
        self.assertEqual(len(result), 0)

        worker = Worker.objects.get(username="mrTommyboy") #should have 0 jobs
        UpdateWorkerDueJobs(worker.id)
        result = GetWorkerActiveJobs(worker.id)
        self.assertEqual(len(result), 0)
        pass

    def test_get_worker_active_and_due_jobs(self):
        worker = Worker.objects.get(username="mrsammy") # should have 0 jobs
        result = GetWorkerActiveAndDueJobs(worker.id)
        self.assertEqual(len(result), 2)


        worker = Worker.objects.get(username="mrwolf") #should have 0 jobs
        result = GetWorkerActiveAndDueJobs(worker.id)
        self.assertEqual(len(result), 0)

        worker = Worker.objects.get(username="mrTommyboy") #should have 1 jobs
        result = GetWorkerActiveAndDueJobs(worker.id)
        self.assertEqual(len(result), 1)
        pass

    def test_get_customer_active_jobs(self):
        customer = Customer.objects.get(username="mrLogan")
        result = GetCustomerActiveJobs(customer.id)
        self.assertEqual(len(result), 1)

        customer = Customer.objects.get(username="mrBoise")
        result = GetCustomerActiveJobs(customer.id)
        self.assertEqual(len(result), 0)
        pass

    def test_get_worker_due_jobs(self):
        worker = Worker.objects.get(username="mrTommyboy")
        result = GetWorkerDueJobs(worker.id)
        self.assertEqual(len(result), 1)
        pass

    def test_get_worker_finished_jobs(self):
        worker = Worker.objects.get(username="mrwolf")
        self.assertEqual(GetWorkerFinishedJobs(worker.id).count(), 1)
        self.assertEqual(GetWorkerFinishedJobs(worker.id).get(address="Finished Job").address, "Finished Job")
        
        workerWithoutJob = Worker.objects.get(username="mrTommyboy")
        self.assertEqual(GetWorkerFinishedJobs(workerWithoutJob.id).count(), 0)

    def test_get_customer_finished_jobs(self):
        customer = Customer.objects.get(username="mrKingOf")
        self.assertEqual(GetCustomerFinishedJobs(customer.id).count(), 2)
        self.assertEqual(GetCustomerFinishedJobs(customer.id).get(address="Finished Job").address, "Finished Job")
        self.assertEqual(GetCustomerFinishedJobs(customer.id).get(address="Testing Finished Job 2").address, "Testing Finished Job 2")
        

    def test_accept_jobs(self):
        worker = Worker.objects.get(username="mrTommyboy")
        job = Job.objects.get(address="Testing 4589 S 4875 N Paris, Idaho")
        self.assertEqual(AcceptJob(worker.id, job.id), True)
        
        job = Job.objects.get(address="Testing 4589 S 4875 N Paris, Idaho")
        self.assertEqual(job.status, 'A')

    def test_delete_job(self):
        job = Job.objects.get(address="Testing 4589 S 4875 N Paris, Idaho")
        self.assertEqual(Job.objects.filter(address="Testing 4589 S 4875 N Paris, Idaho").exists(), True)
        self.assertEqual(DeleteJob(job.id), True)

        self.assertEqual(Job.objects.filter(address="Testing 4589 S 4875 N Paris, Idaho").exists(), False)
        pass

    def test_finish_job(self):
        job = Job.objects.get(address="Testing Townhouses By Macey's")
        
        FinishJob(job.id)

        job = Job.objects.get(address="Testing Townhouses By Macey's")
        owner = Owner.objects.get(username="mrowner")
        customer = Customer.objects.get(username="mrLogan")
        worker = Worker.objects.get(username="mrTommyboy")

        self.assertEqual(job.status, 'F')
        self.assertEqual(customer.balance, 1287.0)
        self.assertEqual(worker.balance, 70.0)
        self.assertEqual(owner.balance, 1002.5) # There are two owners, therefore each owner gets 5%
        pass

    def test_rate_job(self):
        job = Job.objects.get(address="Testing Townhouses By Macey's")
        customer = Customer.objects.get(username="mrLogan")

        RateJob(customer.id, job.id, False)

        customer = Customer.objects.get(username="mrLogan")
        self.assertEqual(customer.averageRating, 0.75)
        self.assertEqual(customer.numberOfRatings, 4)
        pass

    def test_add_completion_time(self):
        job = Job.objects.get(address="Testing Townhouses By Macey's")

        self.assertEqual(job.status == 'F', False)
        self.assertEqual(job.id == Job.objects.filter(customer_id=job.customer_id, status='A').get(address=job.address).id, True)
        self.assertEqual(-0.5, job.completionTime)

        AddCompletionTime(job.id, 1.0)
        job = Job.objects.get(address="Testing Townhouses By Macey's")
        self.assertEqual(1.0, job.completionTime)
        pass


    def test_get_all_jobtypes(self):
        result = GetAllJobTypes()
        self.assertEqual(len(result), 6)
        pass
    
    def test_update_customer_ratings(self):
        customer = Customer.objects.get(username="mrLogan")
        self.assertEqual(customer.averageRating, 1)
        self.assertEqual(customer.numberOfRatings, 3)

        UpdateCustomerRatings(customer.id, 0)

        customer = Customer.objects.get(username="mrLogan")
        self.assertEqual(customer.averageRating, 0.75)
        self.assertEqual(customer.numberOfRatings, 4)
        pass
    
    def test_update_worker_ratings(self):
        worker = Worker.objects.get(username="mrTommyboy")
        self.assertEqual(worker.averageRating, None)

        UpdateWorkerRatings(worker.id, 1)

        worker = Worker.objects.get(username="mrTommyboy")
        self.assertEqual(worker.averageRating, 1)
        pass
    
    def test_update_get_worker_disputed_jobs(self):
        worker = Worker.objects.get(username="mrwolf")
        
        jobs = GetWorkerDisputedJobs(worker.id)
        self.assertEqual(len(jobs), 1)
        pass
    
    def test_dispute_job(self):
        job = Job.objects.get(address="Testing Finished Job 2")
        self.assertEqual(job.status, 'F')

        DisputeJob(job.id)
        job = Job.objects.get(address="Testing Finished Job 2")
        self.assertEqual(job.status, 'I')
        pass
    
    def test_set_job_as_reviewed(self):
        job = Job.objects.get(address="Testing Finished Job 2")
        self.assertEqual(job.status, 'F')

        SetJobAsReviewed(job.id)
        job = Job.objects.get(address="Testing Finished Job 2")
        self.assertEqual(job.status, 'R')
        pass
    
    def test_refund_money(self):
        owner = Owner.objects.get(username="mrowner")
        customer = Customer.objects.get(username="mrKingOf")
        worker = Worker.objects.get(username="mrwolf")
        job = Job.objects.get(address="Testing 1234 Wall Street")
        refundRequest = RefundRequest.objects.get(job_id=job.id)

        self.assertEqual(owner.balance, 1000)
        self.assertEqual(worker.balance, 100000)
        self.assertEqual(customer.balance, 1500)

        RefundMoney(refundRequest.id)

        owner = Owner.objects.get(username="mrowner")
        customer = Customer.objects.get(username="mrKingOf")
        worker = Worker.objects.get(username="mrwolf")

        self.assertEqual(owner.balance, 950)
        self.assertEqual(worker.balance, 99100)
        self.assertEqual(customer.balance, 2500)        
        pass

    def test_close_refund_request(self):
        job = Job.objects.get(address="Testing 1234 Wall Street")
        refundRequest = RefundRequest.objects.get(job_id=job.id)

        self.assertEqual(job.status, "I")
        self.assertEqual(refundRequest.job_id, job.id)

        CloseRefundRequest(refundRequest.id)
        job = Job.objects.get(address="Testing 1234 Wall Street")
        self.assertEqual(job.status, "R")
        self.assertEqual(RefundRequest.objects.filter(job_id=job.id).exists(), False)
        pass
    
    def test_create_customer_account(self):
        self.assertEqual(Customer.objects.filter(username="newCustomer").exists(), False)

        CreateCustomerAccount(username='newCustomer', first_name='First', last_name='Last', email='newCustomer@email.com',password="password1",zipCode=11111, balance=0, phone=1234567899, address=("wicked witch of the west house"))
        self.assertEqual(Customer.objects.filter(username="newCustomer").exists(), True)        
        pass
    
    def test_create_worker_account(self):
        self.assertEqual(Worker.objects.filter(username="newUser").exists(), False)

        CreateWorkerAccount(username='newUser', first_name='First', last_name='Last', email='newUser@email.com', password="password1", zipCode=11111, distance=50, fromTime="0:00", toTime="23:59")
        self.assertEqual(Worker.objects.filter(username="newUser").exists(), True)
        pass
    
    def test_update_worker_settings(self):
        worker = Worker.objects.get(username="mrwolf")
        self.assertEqual(worker.zipCode, 10001)

        UpdateWorkerSettings(worker_id=worker.id, first_name='First', last_name='Last', email='mynewemail@email.com', zipCode=11111, distance=50, jobTypes=[], fromTime="0:00", toTime="23:59")
        worker = Worker.objects.get(username="mrwolf")
        self.assertEqual(worker.zipCode, 11111)        
        pass
    
    def test_update_customer_settings(self):
        customer = Customer.objects.get(username="mrKingOf")
        self.assertEqual(customer.email, "mrManhattan@hotmail.com")
        UpdateCustomerSettings(customer_id=customer.id, first_name='First', last_name='Last', email='theRillDill@iamit.com', zipCode=11111, phoneNumber="111-555-1111", defaultAddress="Homeless")
        customer = Customer.objects.get(username="mrKingOf")
        self.assertEqual(customer.email, 'theRillDill@iamit.com')
        pass

    def test_update_owner_settings(self):
        owner = Owner.objects.get(username="mrowner")
        self.assertEqual(owner.zipCode, 12345)
        UpdateOwnerSettings(owner_id=owner.id, first_name='First', last_name='Last', email='theupdatedemail@email.com', zipCode=11111)
        owner = Owner.objects.get(username="mrowner")
        self.assertEqual(owner.zipCode, 11111)        
        pass