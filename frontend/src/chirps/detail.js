import React, {useState} from "react";
import {ActionBtn} from "./buttons";

export function Chirp(props) {
    const {chirp, didRechirp, hideActions} = props
    const [actionChirp, setActionChirp] = useState(props.chirp ? props.chirp : null)
    const className = props.className ? props.className : 'col-10 mx-auto col-md-6'
    const path = window.location.pathname
    const match = path.match(/(?<chirpid>\d+)/)
    const urlChirpId = match ? match.groups.chirpid : -1
    const isDetail = `${chirp.id}` === `${urlChirpId}`

    const handleLink = (event) => {
        event.preventDefault()
        window.location.href = `/frontend/${chirp.id}`
    }

    const handlePerformAction = (newActionChirp, status) => {
        if (status === 200) {
            setActionChirp(newActionChirp)
        } else if (status === 201) {
            if (didRechirp) {
                didRechirp(newActionChirp)
            }
        }
    }

    return <div className={className}>
        <div>
            <p>{chirp.id} - {chirp.content}</p>
            <ParentChirp chirp={chirp}/>
        </div>
        <div className='btn btn-group'>
            {(actionChirp && hideActions !== true) && <React.Fragment>
                <ActionBtn chirp={actionChirp} didPerformAction={handlePerformAction}
                           action={{type: "chirp", display: chirp.likes + " Chirp"}}/>
                <ActionBtn chirp={actionChirp} didPerformAction={handlePerformAction}
                           action={{type: "unchirp", display: "Unchirp"}}/>
                <ActionBtn chirp={actionChirp} didPerformAction={handlePerformAction}
                           action={{type: "rechirp", display: "Rechirp"}}/>
            </React.Fragment>
            }
            {isDetail === true ? null :
                <button className='btn btn-outline-primary btn-sm' onClick={handleLink}>View</button>}
        </div>

    </div>
}

export function ParentChirp(props) {
    const {chirp} = props
    return chirp.parent ? <div className='row'>
        <div className='col-11 mx-auto p-3 border rounded'>
            <p className='mb-0 text-muted small'>Rechirp</p>
            <Chirp hideActions className={' '} chirp={chirp.parent}/>
        </div>
    </div> : null
}
