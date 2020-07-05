import React, {useEffect, useState} from 'react'
import {ChirpCreate} from "./create";
import {ChirpList, UserFeed} from "./list"
import {apiChirpDetail} from './lookup'
import {Chirp} from './detail'

export function ChirpsComponent(props) {
    const [newChirps, setNewChirps] = useState([])
    const canChirp = (props.canChirp !== undefined && props.canChirp !== null) ? props.canChirp === 'True' : false
    const handleNewChirp = (newChirp) => {
        let tempNewChirps = [...newChirps]
        tempNewChirps.unshift(newChirp)
        setNewChirps(tempNewChirps)
    }
    return <div className={props.className}>
        {canChirp === true && <ChirpCreate didChirp={handleNewChirp} className=''/>}
        <ChirpList newChirps={newChirps} {...props} />
    </div>
}

export function FrontPageComponent(props) {
    const [newChirps, setNewChirps] = useState([])
    const handleNewChirp = (newChirp) => {
        let tempNewChirps = [...newChirps]
        tempNewChirps.unshift(newChirp)
        setNewChirps(tempNewChirps)
    }
    return <div className={props.className}>
        <ChirpCreate didChirp={handleNewChirp} className=''/>
        <ChirpList newChirps={newChirps} {...props} front_page={true} />
    </div>
}

export function ChirpDetailComponent(props) {
    const {chirpId} = props
    const [didLookup, setDidLookup] = useState(false)
    const [chirp, setChirp] = useState(null)

    const handleBackendLookup = (response, status) => {
        if (status === 200) {
            setChirp(response)
        } else {
            alert("There was an error finding your tweet.")
        }
    }
    useEffect(() => {
        if (didLookup === false) {
            apiChirpDetail(chirpId, handleBackendLookup)
            setDidLookup(true)
        }
    }, [chirpId, didLookup, setDidLookup])
    return chirp === null ? null : <Chirp chirp={chirp} className={props.className}/>
}

export function UserFeedComponent(props) {
    const [newChirps] = useState([])
    return <div className={props.className}>
        <UserFeed newChirps={newChirps} {...props}/>
    </div>
}
