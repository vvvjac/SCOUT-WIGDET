// popup.js

// Load existing jobs on popup load
document.addEventListener("DOMContentLoaded", () => {
    loadJobs();
});

// Add a new job when the form is submitted
document.getElementById("jobForm").addEventListener("submit", (e) => {
    e.preventDefault();

    const jobTitle = document.getElementById("jobTitle").value;
    const company = document.getElementById("company").value;
    const status = document.getElementById("status").value;
    const appliedDate = document.getElementById("appliedDate").value;
    const notes = document.getElementById("notes").value;

    const job = { jobTitle, company, status, appliedDate, notes };

    // Save job to Chrome storage
    chrome.storage.local.get({ jobs: [] }, (result) => {
        const jobs = result.jobs;
        jobs.push(job);
        chrome.storage.local.set({ jobs }, () => {
            document.getElementById("jobForm").reset();
            loadJobs();
        });
    });
});

// Load and display jobs from Chrome storage
function loadJobs() {
    chrome.storage.local.get({ jobs: [] }, (result) => {
        const jobList = document.getElementById("jobList");
        jobList.innerHTML = ""; // Clear list

        result.jobs.forEach((job) => {
            const listItem = document.createElement("li");
            listItem.textContent = `${job.jobTitle} at ${job.company} - ${job.status} (Applied on ${job.appliedDate})`;
            jobList.appendChild(listItem);
        });
    });
}
