export function backendLookup(method, endpoint, callback, data) {
    let jsonData;
    if (data) {
        jsonData = JSON.stringify(data)
    }
    const xhr = new XMLHttpRequest()
    const url = '/api/v1/chipper/' + endpoint
    xhr.responseType = "json"
    const csrftoken = Cookies.get('csrftoken');
    xhr.open(method, url)
    xhr.setRequestHeader("Content-Type", "application/json")
    if (csrftoken) {
        xhr.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
        xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
        xhr.setRequestHeader("X-CSRFToken", csrftoken)
    }

    xhr.onload = function () {
        if (xhr.response.results != null && xhr.status === 200) {
            callback(xhr.response.results, xhr.status)
        }
        else if(xhr.status === 201){
            callback(xhr.response, xhr.status)
        }
    }
    xhr.onerror = function (e) {
        console.log(e)
        callback({"message": "The request was an error"}, 400)
    }
    xhr.send(jsonData)
}

export function createTweet(newTweet, callback) {
    lookup("POST", "chirps/", callback, {content: newTweet})
}

export function loadTweets(callback) {
    lookup("GET", "chirps/", callback)
}