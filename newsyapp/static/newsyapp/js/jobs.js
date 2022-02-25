let counter = 0;
const quantity = 30;
let loading = false;

document.addEventListener('DOMContentLoaded', load);

function load() {
    loading = true;
    const start = counter;

    fetch(`/api/get_jobs?start=${start}&quantity=${quantity}`)
    .then(response => response.json())
    .then(jobs => {

        if (jobs.data.length == 0) {
            console.log("No more jobs");
        } else {

            counter += (jobs.data.length < quantity) ? jobs.data.length : quantity;
            
            const jobs_area = document.getElementById("jobs-area");
            for (let i = 0; i < jobs.data.length; i++) {
                jobs_area.append(spawnJob(jobs.data[i]));
            }
        }

    });
    loading = false;
}

function spawnJob(job) {
    const col_div = document.createElement('div');
    col_div.classList.add("col");

    const job_div = document.createElement('div');
    job_div.classList.add("h-100", "p-5", "text-white", "bg-dark", "rounded-3");

    const h4 = document.createElement('h4');
    h4.innerHTML = job.title;
    job_div.append(h4);

    const p1 = document.createElement('p');
    p1.classList.add("text-muted");
    p1.innerHTML = getElapsedTime(job.time);
    job_div.append(p1);

    const p2 = document.createElement('p');
    p2.innerHTML = `Posted by ${job.by}`;
    job_div.append(p2);

    const a = document.createElement('a');
    
    const button = document.createElement('button');
    button.classList.add("btn", "btn-outline-light");
    button.type = "button";
    const btn_txt_node = document.createTextNode("View job");
    button.appendChild(btn_txt_node);
    
    a.appendChild(button);

    let url = document.getElementById("Url").dataset.url;
    url = url.replace('0000', `${job.id}`);
    a.href = url;
    job_div.append(a);

    col_div.append(job_div);

    return col_div;
}

function getElapsedTime(created_time) {
    let elapsed_seconds = Math.floor(Date.now() / 1000) - created_time;
    
    if (elapsed_seconds < 60) {
        return `${elapsed_seconds} s`;
    } else if (elapsed_seconds < 3600) {
        return `${Math.floor(elapsed_seconds / 60)} min`;
    } else if (elapsed_seconds < 86400) {
        return `${Math.floor(elapsed_seconds / 3600)} h`;
    } else if (elapsed_seconds < 2592000) {
        let elapsed_time = Math.floor(elapsed_seconds / 86400);
        let adj = (elapsed_time > 1) ? " days" : " day";
        return elapsed_time + adj;
    } else if (elapsed_seconds < 31104000) {
        let elapsed_time = Math.floor(elapsed_seconds / 2592000);
        let adj = (elapsed_time > 1) ? " months" : " month";
        return elapsed_time + adj;
    } else {
        let elapsed_time = Math.floor(elapsed_seconds / 31104000);
        let adj = (elapsed_time > 1) ? " years" : " year";
        return elapsed_time + adj;
    }
}

window.onscroll = function() {
    if (((window.innerHeight + window.pageYOffset) >= document.body.offsetHeight - 10) && !loading) {
            load();
    }
};
