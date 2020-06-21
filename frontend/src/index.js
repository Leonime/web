import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';
import {ChirpDetailComponent, ChirpsComponent} from "./chirps";

const appEl = document.getElementById('root')
if (appEl) {
    ReactDOM.render(<App/>, appEl);
}
const e = React.createElement
const chirpsEl = document.getElementById("chirp")
if (chirpsEl) {
    ReactDOM.render(
        e(ChirpsComponent, chirpsEl.dataset), chirpsEl);
}

const chirpDetailElements = document.querySelectorAll(".chirp-detail")

chirpDetailElements.forEach(container => {
    ReactDOM.render(
        e(ChirpDetailComponent, container.dataset),
        container);
})

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
