import React, {useEffect, useState} from 'react';


function loadTweets(callback) {
    const xhr = new XMLHttpRequest()
    const method = 'GET'
    const url = "/api/v1/chipper/chirps/"
    xhr.responseType = "json"
    xhr.open(method, url)
    xhr.onload = function () {
        callback(xhr.response.results, xhr.status)
    }
    xhr.onerror = function (e) {
        console.log(e)
        callback({"message": "The request was an error"}, 400)
    }
    xhr.send()
}

function Tweet(props) {
    const {tweet} = props
    const className = props.className ? props.className : 'col-5 mx-auto col-md-3 align-self-center'
    return <div className={className}>
        <p>{tweet.id} - {tweet.content}</p>
    </div>
}

function App() {
    const [tweets, setTweets] = useState([])

    useEffect(() => {
        const myCallback = (response, status) => {
            console.log(response, status)
            if (status === 200) {
                setTweets(response)
            } else {
                alert("There was an error")
            }
        }
        loadTweets(myCallback)
    }, [])
    return (
        <div className="App">
            <header className="App-header container col-sm-12">
                <div className='row justify-content-md-center'>
                    {tweets.map((item, index) => {
                        return <Tweet tweet={item} className='row col-sm-5 my-3 py-3 border bg-white text-dark'
                                      key={`${index}-{item.id}`}/>
                    })}
                </div>
            </header>
        </div>
    );
}

export default App;
