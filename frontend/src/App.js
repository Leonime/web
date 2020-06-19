import React from "react";
import {ChirpsComponent} from './chirps'

function App() {
    return (
        <div className="App">
            <header className="App-header container col-sm-12">
                <div className='row justify-content-md-center'>
                    <ChirpsComponent/>
                </div>
            </header>
        </div>
    );
}

export default App;
