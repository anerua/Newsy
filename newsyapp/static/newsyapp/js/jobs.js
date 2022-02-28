let counter = 0;
const quantity = 30;
let loading = false;
let completed = false;
var myBtn;

document.addEventListener('DOMContentLoaded', () => {
    myBtn = document.getElementById("btn-back-to-top");
    myBtn.addEventListener("click", backToTop);
    load();
});


function load() {
    loading = true;
    const start = counter;

    if (!completed) {
        document.getElementById("loading-symbol").style.display = "block";
    }

    fetch(`/api/get_jobs?start=${start}&quantity=${quantity}`)
    .then(response => response.json())
    .then(jobs => {

        if (jobs.data.length != 0) {

            counter += (jobs.data.length < quantity) ? jobs.data.length : quantity;
            
            const jobs_area = document.getElementById("jobs-area");
            for (let i = 0; i < jobs.data.length; i++) {
                jobs_area.append(spawnJob(jobs.data[i]));
            }
        } else {
            completed = true;
        }
        document.getElementById("loading-symbol").style.display = "none";
        loading = false;
    });
}


function spawnJob(job) {
    const colDiv = document.createElement('div');
    colDiv.classList.add("col");

    const jobDiv = document.createElement('div');
    jobDiv.classList.add("h-100", "p-5", "text-white", "bg-dark", "rounded-3");

    const h4 = document.createElement('h4');
    h4.innerHTML = job.title;
    jobDiv.append(h4);

    const p1 = document.createElement('p');
    p1.classList.add("text-muted");
    p1.innerHTML = getElapsedTime(job.time);
    jobDiv.append(p1);

    const p2 = document.createElement('p');
    p2.innerHTML = `Posted by ${job.by}`;
    jobDiv.append(p2);

    const a = document.createElement('a');
    
    const button = document.createElement('button');
    button.classList.add("btn", "btn-outline-light");
    button.type = "button";
    const btnTextNode = document.createTextNode("View job");
    button.appendChild(btnTextNode);
    
    a.appendChild(button);

    let url = document.getElementById("Url").dataset.url;
    url = url.replace('0000', `${job.id}`);
    a.href = url;
    jobDiv.append(a);

    colDiv.append(jobDiv);

    return colDiv;
}


function getElapsedTime(createdTime) {
    let elapsedSeconds = Math.floor(Date.now() / 1000) - createdTime;
    
    if (elapsedSeconds < 60) {
        return `${elapsedSeconds} s`;
    } else if (elapsedSeconds < 3600) {
        return `${Math.floor(elapsedSeconds / 60)} min`;
    } else if (elapsedSeconds < 86400) {
        return `${Math.floor(elapsedSeconds / 3600)} h`;
    } else if (elapsedSeconds < 2592000) {
        let elapsedTime = Math.floor(elapsedSeconds / 86400);
        let adj = (elapsedTime > 1) ? " days" : " day";
        return elapsedTime + adj;
    } else if (elapsedSeconds < 31104000) {
        let elapsedTime = Math.floor(elapsedSeconds / 2592000);
        let adj = (elapsedTime > 1) ? " months" : " month";
        return elapsedTime + adj;
    } else {
        let elapsedTime = Math.floor(elapsedSeconds / 31104000);
        let adj = (elapsedTime > 1) ? " years" : " year";
        return elapsedTime + adj;
    }
}


window.onscroll = function() {
    if (((window.innerHeight + window.pageYOffset) >= document.body.offsetHeight - 10) && !loading) {
        load();
    }
    toggleTopBtn();
};


function toggleTopBtn() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
      myBtn.style.display = "block";
    } else {
      myBtn.style.display = "none";
    }
}
  
  
function backToTop() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
 }
