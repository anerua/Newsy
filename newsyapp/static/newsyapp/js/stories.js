let counter = 0;
const quantity = 30;

document.addEventListener('DOMContentLoaded', load);

function load() {
    const start = counter;
    counter += quantity;

    fetch(`/api/get_stories?start=${start}&quantity=${quantity}`)
    .then(response => response.json())
    .then(stories => {
        const stories_area = document.getElementById("stories-area");
        for (let i = 0; i < stories.data.length; i++) {
            stories_area.append(spawnStory(stories.data[i]));
        }
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
    p1.innerHTML = story.descendants ? `${story.descendants} comments.` : "0 comments.";
    story_div.append(p1);

    const p2 = document.createElement('p');
    p2.innerHTML = story.time;
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
    url = url.replace('0000', `${story.id}`)
    a.href = url;
    story_div.append(a);

    col_div.append(story_div);

    return col_div;
}

// window.onscroll = () => {
//     if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
//         load();
//     }
// }

$(window).scroll(function() {
    if($(window).scrollTop() + $(window).height() == $(document).height()) {
        load();
    }
 });
