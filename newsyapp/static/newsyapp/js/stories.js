let counter = 0;
const quantity = 30;
let loading = false;
let completed = false;

document.addEventListener('DOMContentLoaded', load);


function load() {
    loading = true;
    const start = counter;

    if (!completed) {
        document.getElementById("loading-symbol").style.display = "block";
    }

    fetch(`/api/get_stories?start=${start}&quantity=${quantity}`)
    .then(response => response.json())
    .then(stories => {

        if (stories.data.length != 0) {

            const storiesArea = document.getElementById("stories-area");
            for (let i = 0; i < stories.data.length; i++) {
                storiesArea.append(spawnStory(stories.data[i]));
            }

            counter += (stories.data.length < quantity) ? stories.data.length : quantity;
        } else {
            completed = true;
        }
        document.getElementById("loading-symbol").style.display = "none";
        loading = false;
    });
}


function spawnStory(story) {
    const colDiv = document.createElement('div');
    colDiv.classList.add("col");

    const storyDiv = document.createElement('div');
    storyDiv.classList.add("h-100", "p-5", "text-white", "bg-dark", "rounded-3");

    const h4 = document.createElement('h4');
    h4.innerHTML = story.title;
    storyDiv.append(h4);

    const p1 = document.createElement('p');
    p1.innerHTML = getElapsedTime(story.time);
    p1.classList.add("text-muted");
    storyDiv.append(p1);

    const p2 = document.createElement('p');
    p2.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chat-square-text-fill" viewBox="0 0 16 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-2.5a1 1 0 0 0-.8.4l-1.9 2.533a1 1 0 0 1-1.6 0L5.3 12.4a1 1 0 0 0-.8-.4H2a2 2 0 0 1-2-2V2zm3.5 1a.5.5 0 0 0 0 1h9a.5.5 0 0 0 0-1h-9zm0 2.5a.5.5 0 0 0 0 1h9a.5.5 0 0 0 0-1h-9zm0 2.5a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1h-5z"/></svg>';
    p2.innerHTML += story.descendants ? ` ${story.descendants}` : " 0";
    storyDiv.append(p2);

    const p3 = document.createElement('p');
    p3.innerHTML = `Posted by ${story.by}`;
    storyDiv.append(p3);

    const a = document.createElement('a');
    
    const button = document.createElement('button');
    button.classList.add("btn", "btn-outline-light");
    button.type = "button";
    const btnTextNode = document.createTextNode("View story");
    button.appendChild(btnTextNode);
    
    a.appendChild(button);

    let url = document.getElementById("Url").dataset.url;
    url = url.replace('0000', `${story.id}`);
    a.href = url;
    storyDiv.append(a);

    colDiv.append(storyDiv);

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
};