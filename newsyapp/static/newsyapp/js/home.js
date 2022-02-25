document.addEventListener('DOMContentLoaded', () => {
    const timeElements = document.querySelectorAll(".elapsed-time");
    timeElements.forEach(element => {
        const createdTime = element.dataset.time;
        element.innerHTML = getElapsedTime(createdTime);
    });
});


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