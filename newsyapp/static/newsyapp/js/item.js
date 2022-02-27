document.addEventListener('DOMContentLoaded', () => {
    document.getElementById("loading-symbol").style.display = "none";
    const commentTimeP = document.getElementById('comment-time-p');
    commentTimeP.innerHTML = getElapsedTime(commentTimeP.dataset.time);
    getComments();
});


function getComments() {

    const descendants = parseInt(document.getElementById('descendants-data').textContent);

    const comments_area = document.getElementById('comments-area');
    if (descendants) {
        document.getElementById("loading-symbol").style.display = "block";

        const item_id = parseInt(document.getElementById('id-data').textContent);
        fetch(`https://hacker-news.firebaseio.com/v0/item/${item_id}.json?print=pretty`)
        .then(response => response.json())
        .then(data => {

            const item_kids = data.kids;
            item_kids.forEach(kid => {
                const div = create_conversation(kid, 0);
                const hr = document.createElement('hr');
                div.append(hr);
                comments_area.append(div);
            });
            document.getElementById("loading-symbol").style.display = "none";
        });

    } else {
        comments_area.append("No comments.");
    }

}


function create_conversation(kid, level) {
    const div = document.createElement('div');
    fetch(`https://hacker-news.firebaseio.com/v0/item/${kid}.json?print=pretty`)
    .then(response => response.json())
    .then(comment => {

        div.style.marginLeft = `${level * 2}%`;
        if (comment.text) {
            const p0 = document.createElement('p');
            p0.classList.add("text-muted");
            p0.innerHTML = `${comment.by} | ${getElapsedTime(comment.time)}`
            div.append(p0);

            const p1 = document.createElement('p');
            p1.innerHTML = comment.text;
            div.append(p1);

            if (("kids" in comment) && comment.kids.length) {
                console.log(`These: ${comment.kids}`)
                const comment_kids = comment.kids;
                comment_kids.forEach(kid => {
                    div.append(create_conversation(kid, level + 1));
                });
            }
        }
    });
    return div;
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