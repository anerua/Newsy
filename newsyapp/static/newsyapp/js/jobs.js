let counter = 0;
const quantity = 30;

document.addEventListener('DOMContentLoaded', load);

function load() {
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
    p1.innerHTML = job.time;
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
    url = url.replace('0000', `${job.id}`)
    a.href = url;
    job_div.append(a);

    col_div.append(job_div);

    return col_div;
}

// $(window).scroll(function() {
//     if( $(window).scrollTop() ==  $(document).height() - $(window).height()) {
//         load();
//     }
//  });

window.onscroll = function(ev) {
    let docHeight = window.innerHeight + window.pageYOffset;
    if ((docHeight >= document.body.offsetHeight - 10) && (docHeight <= document.body.offsetHeight) ) {
        load();
    }
};
