document.addEventListener('DOMContentLoaded', () => {
    const timeElements = document.querySelectorAll(".elapsed-time");
    timeElements.forEach(element => {
        const createdTime = element.dataset.time;
        element.innerHTML = getElapsedTime(createdTime);
    });
});


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