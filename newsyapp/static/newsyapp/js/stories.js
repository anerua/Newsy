let counter = 0;
const quantity = 30;
let loading = false;

document.addEventListener('DOMContentLoaded', load);

function load() {
    loading = true;
    const start = counter;
    document.getElementById("loading-symbol").style.display = "block";

    fetch(`/api/get_stories?start=${start}&quantity=${quantity}`)
    .then(response => response.json())
    .then(stories => {
        
        if (stories.data.length != 0) {

            const stories_area = document.getElementById("stories-area");
            for (let i = 0; i < stories.data.length; i++) {
                stories_area.append(spawnStory(stories.data[i]));
            }

            counter += (stories.data.length < quantity) ? stories.data.length : quantity;
        }
        document.getElementById("loading-symbol").style.display = "none";
        loading = false;
    });
}


function spawnStory(story) {
    const col_div = document.createElement('div');
    col_div.classList.add("col");

    const story_div = document.createElement('div');
    story_div.classList.add("h-100", "p-5", "text-white", "bg-dark", "rounded-3");

    const h4 = document.createElement('h4');
    h4.innerHTML = story.title;
    story_div.append(h4);

    const p1 = document.createElement('p');
    p1.innerHTML = getElapsedTime(story.time);
    p1.classList.add("text-muted");
    story_div.append(p1);

    const p2 = document.createElement('p');
    p2.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chat-square-text-fill" viewBox="0 0 16 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-2.5a1 1 0 0 0-.8.4l-1.9 2.533a1 1 0 0 1-1.6 0L5.3 12.4a1 1 0 0 0-.8-.4H2a2 2 0 0 1-2-2V2zm3.5 1a.5.5 0 0 0 0 1h9a.5.5 0 0 0 0-1h-9zm0 2.5a.5.5 0 0 0 0 1h9a.5.5 0 0 0 0-1h-9zm0 2.5a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1h-5z"/></svg>';
    p2.innerHTML += story.descendants ? ` ${story.descendants}` : " 0";
    story_div.append(p2);

    const p3 = document.createElement('p');
    p3.innerHTML = `Posted by ${story.by}`;
    story_div.append(p3);

    const a = document.createElement('a');
    
    const button = document.createElement('button');
    button.classList.add("btn", "btn-outline-light");
    button.type = "button";
    const btn_txt_node = document.createTextNode("View story");
    button.appendChild(btn_txt_node);
    
    a.appendChild(button);

    let url = document.getElementById("Url").dataset.url;
    url = url.replace('0000', `${story.id}`);
    a.href = url;
    story_div.append(a);

    col_div.append(story_div);

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