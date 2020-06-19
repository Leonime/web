import React from "react";
import {TweetsComponent} from './chirps'

function App() {
    return (
        <div className="App">
            <header className="App-header container col-sm-12">
                <div className='row justify-content-md-center'>
                    <TweetsComponent/>
                </div>
            </header>
        </div>
    );
}

export default App;
