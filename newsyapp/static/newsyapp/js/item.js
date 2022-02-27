document.addEventListener('DOMContentLoaded', () => {
    document.getElementById("loading-symbol").style.display = "none";
    const commentTimeP = document.getElementById('comment-time-p');
    commentTimeP.innerHTML = getElapsedTime(commentTimeP.dataset.time);
    getComments();
});


function getComments() {

    const descendants = parseInt(document.getElementById('descendants-data').textContent);

    const commentsArea = document.getElementById('comments-area');
    if (descendants) {
        document.getElementById("loading-symbol").style.display = "block";

        const itemID = parseInt(document.getElementById('id-data').textContent);
        fetch(`https://hacker-news.firebaseio.com/v0/item/${itemID}.json?print=pretty`)
        .then(response => response.json())
        .then(data => {

            const itemKids = data.kids;
            itemKids.forEach(kid => {
                const div = createConversation(kid, 0);
                const hr = document.createElement('hr');
                div.append(hr);
                commentsArea.append(div);
            });
            document.getElementById("loading-symbol").style.display = "none";
        });

    } else {
        commentsArea.append("No comments.");
    }

}


function createConversation(kid, level) {
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
                const commentKids = comment.kids;
                commentKids.forEach(kid => {
                    div.append(createConversation(kid, level + 1));
                });
            }
        }
    });
    return div;
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