document.addEventListener('DOMContentLoaded', () => {
    getComments();
});


function getComments() {

    const descendants = parseInt(document.getElementById('descendants-data').textContent);

    if (descendants) {
        const comments_area = document.getElementById('comments-area');
        const item_id = parseInt(document.getElementById('id-data').textContent);
        fetch(`https://hacker-news.firebaseio.com/v0/item/${item_id}.json?print=pretty`)
        .then(response => response.json())
        .then(data => {

            const item_kids = data.kids;
            item_kids.forEach(kid => {
                fetch(`https://hacker-news.firebaseio.com/v0/item/${kid}.json?print=pretty`)
                .then(response => response.json())
                .then(comment => {

                    if (comment.text) {
                        const div = document.createElement('div');
                        div.append(`${comment.by} | ${comment.time}`);

                        const p1 = document.createElement('p');
                        p1.innerHTML = comment.text;
                        p1.classList.add("text-success");
                        div.append(p1);

                        const hr = document.createElement('hr');
                        div.append(hr);

                        comments_area.append(div);
                    }

                   
                });
            });
        });
    }
}