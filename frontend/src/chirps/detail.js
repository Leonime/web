import React, {useState} from "react";
import {ActionBtn} from "./buttons";
import {UserDisplay, UserPicture} from "../profiles";
import {ProfilePicture} from "../profiles/components";

export function Chirp(props) {
    const {chirp, didRechirp, hideActions, isRechirp, rechirper} = props
    const [actionChirp, setActionChirp] = useState(props.chirp ? props.chirp : null)
    let className = props.className ? props.className : 'col-10 mx-auto col-md-6'
    className = isRechirp === true ? `${className} p-2 border border-dark rounded` : className
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
        {isRechirp === true && <div className='mb-2'>
            <span className='small text-muted'>Rechirp via <UserDisplay user={rechirper}/></span>
        </div>}
        <div className='d-flex'>
            <div className=''>
                <ProfilePicture user={chirp.user}/>
            </div>
            <div className='col-11'>
                <div>
                    <p>
                        <UserDisplay includeFullName user={chirp.user}/>
                    </p>
                    <p>{chirp.content}</p>
                    <ParentChirp chirp={chirp} rechirper={chirp.user}/>
                </div>
                <div className='btn btn-group px-0'>
                    {(actionChirp && hideActions !== true) && <React.Fragment>
                        <ActionBtn chirp={actionChirp} didPerformAction={handlePerformAction}
                                   action={{type: "chirp", display: "Chirp"}}/>
                        <ActionBtn chirp={actionChirp} didPerformAction={handlePerformAction}
                                   action={{type: "unchirp", display: "Unchirp"}}/>
                        <ActionBtn chirp={actionChirp} didPerformAction={handlePerformAction}
                                   action={{type: "rechirp", display: "Rechirp"}}/>
                    </React.Fragment>
                    }
                    {isDetail === true ? null :
                        <button className='btn btn-dark btn-sm' onClick={handleLink}>View</button>}
                </div>
            </div>
        </div>
    </div>
}

export function ParentChirp(props) {
    const {chirp} = props
    return chirp.parent ?
        <Chirp isRechirp rechirper={props.rechirper} hideActions className={' '} chirp={chirp.parent}/> : null
}
