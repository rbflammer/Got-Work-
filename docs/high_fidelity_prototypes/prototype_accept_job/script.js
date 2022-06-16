availableDiv = document.querySelector('.available-jobs');
availableList = document.getElementById("available-jobs__list");
currentDiv = document.querySelector('.current-jobs');
currentList = document.getElementById('current-jobs__list');

class Job{
    constructor(id, contact, type, location, pay, accepted) {
        this.id = id;
        this.contact = contact;
        this.type = type;
        this.location = location;
        this.pay = pay;
    }
}

function documentSetup(){
    const jobs = [];
    job1 = new Job(0, "email@something.com", "mowing", "North Logan", 80, false);
    job2 = new Job(1, "(435)-555-3827", "shoveling", "Wellsville", 85, false);
    job3 = new Job(2, "pls don't talk to me", "Being Awesome", "Everywhere", 1000, false);
    jobs.push(job1);
    jobs.push(job2);
    jobs.push(job3);

    console.log(jobs);
    
    for (job of jobs){
        console.log(job);
        newJob(job);
    }
    
    if (jobs.length >= 0){
        alert("There are " + jobs.length + " jobs available nearby!");
    }
}

function newJob(job) {
    var jobDiv = createJobDiv(job, "available-job__div");
    acceptButton = document.createElement("input");
    acceptButton.setAttribute("type", "button");
    acceptButton.setAttribute("name", "accept");
    acceptButton.setAttribute("class", "accept-button");
    acceptButton.setAttribute("value", "Accept Job");
    acceptButton.setAttribute("onclick", "acceptJob(this.parentElement)");

    declineButton = document.createElement("input");
    declineButton.setAttribute("type", "button");
    declineButton.setAttribute("name", "decline");
    declineButton.setAttribute("class", "decline-button");
    declineButton.setAttribute("value", "Decline Job");
    declineButton.setAttribute("onclick", "declineJob(this.parentElement)");
    
    jobDiv.appendChild(acceptButton);
    jobDiv.appendChild(declineButton);


    availableList.appendChild(jobDiv);
    
}

function acceptJob(jobDiv) {
    job = new Job(jobDiv.dataset.jobId, jobDiv.dataset.jobContact, jobDiv.dataset.jobType, jobDiv.dataset.jobLocation, jobDiv.dataset.jobPay, true);
    console.log(jobDiv.dataset);
    console.log("Job " + job.type + " accepted");    
    availableList.removeChild(jobDiv);
    jobDiv = createJobDiv(job, "current-job__div");
    
    finishedButton = document.createElement("input");
    finishedButton.setAttribute("type", "button");
    finishedButton.setAttribute("name", "accept");
    finishedButton.setAttribute("class", "finished-button");    
    finishedButton.setAttribute("value", "Finished!");
    finishedButton.setAttribute("onclick", "finishJob(this.parentElement)");

    reportProblemButton = document.createElement("input");
    reportProblemButton.setAttribute("type", "button");
    reportProblemButton.setAttribute("name", "reportProblem");
    reportProblemButton.setAttribute("class", "report-problem-button");
    reportProblemButton.setAttribute("value", "Report A Problem");
    reportProblemButton.setAttribute("onclick", "reportProblem(this.parentElement)");

    jobDiv.appendChild(finishedButton);
    jobDiv.appendChild(reportProblemButton);
    currentList.appendChild(jobDiv);
}


//creates a basic job div describing basic into. No buttons included.
function createJobDiv(job, className) {
    jobDiv = document.createElement("div");
    jobDiv.setAttribute("class", "available-job__div");
    jobDiv.setAttribute("data-job-id", job.id);
    jobDiv.setAttribute("data-job-contact", job.contact);
    jobDiv.setAttribute("data-job-type", job.type);
    jobDiv.setAttribute("data-job-location", job.location);
    jobDiv.setAttribute("data-job-pay", job.pay);
    
    var p1 = document.createElement("h4");
    var p2 = document.createElement("p");
    var p3 = document.createElement("p");
    p1.setAttribute("class", "job-description");
    p2.setAttribute("class", "job-description");
    p3.setAttribute("class", "job-description");
    p1.textContent = "Type: " + job.type;
    p2.textContent = "Location: " + job.location;
    p3.textContent = "Pay: " + job.pay;

    jobDiv.appendChild(p1);
    jobDiv.appendChild(p2);
    jobDiv.appendChild(p3);

    return jobDiv;
}


function declineJob(jobDiv) {
    jobDiv.parentElement.removeChild(jobDiv);
}

function finishJob(jobDiv) {
    console.log("This will give the worker a notification on their end by reporting to the database that the job is finished");
    currentList.removeChild(jobDiv);
}

function reportProblem(jobDiv) {
    console.log("This will POST to the database");

    jobDiv.setAttribute("style", `background-color: rgb(0, 255, 255)`);
    //last child should be "report problem" button.

    //removeReportButton = document.createElement("input");
    //removeReportButton.setAttribute("type", "button");
    //removeReportButton.setAttribute("class", "remove-report-button");
    //removeReportButton.setAttribute("onclick", "removeReport(this.parentElement)");
    
    //jobDiv.replaceChild(removeReportButton, jobDiv.lastChild);
    contactField = document.createElement("span");
    contactField.setAttribute("class", "contact-field");
    contactField.textContent = "Constact at " + jobDiv.dataset.jobContact;

    newP = document.createElement("p");
    newP.setAttribute("class", "problem-report__text");
    newP.textContent = "A notification has been sent to the client. You have reported a problem with this job, and it is currently under review by the client.";

    jobDiv.insertBefore(newP, jobDiv.firstChild);
    jobDiv.replaceChild(contactField, jobDiv.lastChild);
    
}


documentSetup();
