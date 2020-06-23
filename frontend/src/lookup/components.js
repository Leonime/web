export function backendLookup(method, endpoint, callback, data) {
    let jsonData;
    if (data) {
        jsonData = JSON.stringify(data)
    }
    const xhr = new XMLHttpRequest()
    const url = endpoint
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
        if(xhr.status === 201 || xhr.status === 200) {
            callback(xhr.response, xhr.status)
        }
        else if(xhr.status === 403) {
            window.location.href = "/login?showLoginRequired=true"
        }
    }
    xhr.onerror = function (e) {
        console.log(e)
        callback({"message": "The request was an error"}, 400)
    }
    xhr.send(jsonData)
}
