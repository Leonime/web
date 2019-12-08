let dots = 1;
const progressTitle = document.getElementById('progress-title');
updateProgressTitle();

const timer = setInterval(function () {
    updateProgressTitle();
    axios.get(taskUrl)
        .then(function (response) {
            const taskStatus = response.data.task_status;
            if (taskStatus === 'SUCCESS') {
                clearTimer('Check downloads for results');
                const url = window.location.protocol + '//' + window.location.host + response.data.results.archive_path;
                const a = document.createElement("a");
                a.target = '_BLANK';
                document.body.appendChild(a);
                a.style = "display:none";
                a.href = url;
                a.download = 'results.zip';
                a.click();
                document.body.removeChild(a);
            } else if (taskStatus === 'FAILURE') {
                clearTimer('An error occurred');
            }
        })
        .catch(function (err) {
            console.log('err', err);
            clearTimer('An error occurred');
        });
}, 800);

function updateProgressTitle() {
    dots++;
    if (dots > 3) {
        dots = 1;
    }
    progressTitle.innerHTML = 'processing images ';
    for (let i = 0; i < dots; i++) {
        progressTitle.innerHTML += '.';
    }
}

function clearTimer(message) {
    clearInterval(timer);
    progressTitle.innerHTML = message;
}