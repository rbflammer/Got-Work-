from django.urls import path, include
from . import views

app_name = 'jobs'
urlpatterns = [
    path('', views.frontPage, name='frontPage'),
    path('sign_up/generic', views.genericSignUp, name='genericSignUp'),
    path('sign_up/worker', views.workerSignUp, name='workerSignUp'),
    path('sign_up/customer', views.customerSignUp, name='customerSignUp'),

    path('user/', views.userHome, name="userHome"),
    path('worker/', views.workerHome, name='workerHome'), #URL Format: hostname/worker/<worker_id>/
    path('accept/<int:job_id>/<int:worker_id>/', views.acceptJob, name='acceptJob'), #URL Format: hostname/<job_id>/<worker_id>/ #For post requests
    path('finish/<int:job_id>/', views.finishJob, name='finishJob'), #URL Format: hostname/<job_id>/<worker_id>/ #For post requests
    
    path('customer/', views.customerHome, name='customerHome'), #URL Format: hostname/worker/<worker_id>/
    path('delete/<int:job_id>/', views.deleteJob, name='deleteJob'), #URL Format: hostname/<job_id>/ #For post requests
    path('createjob/<int:customer_id>/', views.createJob, name='createJob'),
    path('createjob/<int:customer_id>/<str:error>/', views.createJob, name='createJob'),
    path('createjobtype/<int:owner_id>/', views.createJobType, name='createJobType'),
    path('createjobtype/<int:owner_id>/<str:error>/', views.createJobType, name='createJobType'),
    path('save_job/<int:customer_id>/', views.saveJob, name='saveJob'),
    path('save_job_type/<int:owner_id>/', views.saveJobType, name='saveJobType'),
    path('reviewworker/<int:job_id>/', views.reviewWorker, name='reviewWorker'),
    path('approvedenyrequest/<int:request_id>/<int:owner_id>/', views.approveDenyRequest, name='approveDenyRequest'),

    path('owner/<str:message>/', views.ownerHome, name='ownerHome'),
    path('owner/', views.ownerHome, name='ownerHome'),
    
    path('worker/<int:worker_id>/settings', views.workerSettings, name='workerSettings'),
    path('customer/<int:customer_id>/settings', views.customerSettings, name='customerSettings'),
    path('owner/<int:owner_id>/settings', views.ownerSettings, name='ownerSettings'),

    path('postworkersettings/<int:worker_id>/', views.postWorkerSettings, name='postWorkerSettings'),
    path('postcustomersettings/<int:customer_id>/', views.postCustomerSettings, name='postCustomerSettings'),
    path('postownersettings/<int:owner_id>/', views.postOwnerSettings, name='postOwnerSettings'),

    path('deposit/worker/<int:user_id>/', views.depositWorker, name='depositWorker'),
    path('withdraw/worker/<int:user_id>/', views.withdrawWorker, name='withdrawWorker'),
    path('deposit/customer/<int:user_id>/', views.depositCustomer, name='depositCustomer'),
    path('withdraw/customer/<int:user_id>/', views.withdrawCustomer, name='withdrawCustomer'),
    path('deposit/owner/<int:user_id>/', views.depositOwner, name='depositOwner'),
    path('withdraw/owner/<int:user_id>/', views.withdrawOwner, name='withdrawOwner'),
    
    path('utilitytestworker/<int:worker_id>/', views.utilityTestWorker, name='utilityTestWorker'),
    path('utilitytestcustomer/<int:customer_id>/', views.utilityTestCustomer, name='utilityTestCustomer'),
    # path('get_active_jobs', views.get_active_jobs, name="get_active_jobs"), #URL Format: hostname/get_active_jobs?id=USER_ID
    path('customer_sign_up', views.postCustomer, name='postCustomer'),
    path('worker_sign_up', views.createWorker, name='createWorker'),
    path('front_page', views.logIn, name='logIn'),

    path('logout/', views.Logout, name="logout")
]
