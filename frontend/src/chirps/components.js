import React, {useEffect, useState} from 'react'
import {ChirpCreate} from "./create";
import {ChirpList} from "./list"
import {apiChirpDetail} from './lookup'
import {Chirp} from './detail'

export function ChirpsComponent(props) {
    const [newChirps, setNewChirps] = useState([])
    const canChirp = props.canChirp !== "false"
    const handleNewChirp = (newChirp) => {
        let tempNewChirps = [...newChirps]
        tempNewChirps.unshift(newChirp)
        setNewChirps(tempNewChirps)
    }
    return <div className={props.className}>
        {canChirp === true && <ChirpCreate didChirp={handleNewChirp} className='col-12 mb-3'/>}
        <ChirpList newChirps={newChirps} {...props} />
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
