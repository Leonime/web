import React from "react";
import {apiChirpAction} from "./lookup";
import numeral from "numeral";

export function ActionBtn(props) {
    const {chirp, action, didPerformAction} = props
    const likes = chirp.likes ? chirp.likes : 0
    const className = props.className ? props.className : 'btn btn-primary btn-sm'
    const actionDisplay = action.type === 'chirp' ? likes > 1 ? action.display + 's' : action.display : action.display ? action.display : 'Action'

    const handleActionBackendEvent = (response, status) => {
        if ((status === 200 || status === 201) && didPerformAction) {
            didPerformAction(response, status)
        }
    }
    const handleClick = (event) => {
        event.preventDefault()
        apiChirpAction(chirp.id, action.type, handleActionBackendEvent)
    }
    const display = action.type === 'chirp' ? <span><span className="badge badge-dark">{numeral(likes).format("0 a")}</span> {actionDisplay}</span> : actionDisplay
    return <button className={className} onClick={handleClick}>{display}</button>
}
