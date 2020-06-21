import React, {useEffect, useState} from "react";
import {apiChirpList} from "./lookup";
import {Chirp} from "./detail";

export function ChirpList(props) {
    const [chirpsInit, setChirpsInit] = useState([])
    const [chirps, setChirps] = useState([])
    const [chirpsDidSet, setChirpsDidSet] = useState(false)
    useEffect(() => {
        const final = [...props.newChirps].concat(chirpsInit)
        if (final.length !== chirps.length) {
            setChirps(final)
        }
    }, [props.newChirps, chirps, chirpsInit])

    useEffect(() => {
        if (chirpsDidSet === false) {
            const handleChirpListLookup = (response, status) => {
                if (status === 200) {
                    setChirpsInit(response)
                    setChirpsDidSet(true)
                } else {
                    alert("There was an error")
                }
            }
            apiChirpList(props.username, handleChirpListLookup)
        }
    }, [chirpsInit, chirpsDidSet, setChirpsDidSet, props.username])

    const handleDidRechirp = newChirp => {
        const updateChirpsInit = [...chirpsInit]
        updateChirpsInit.unshift(newChirp)
        setChirpsInit(updateChirpsInit)
        const updateFinalChirps = [...chirps]
        updateFinalChirps.unshift(chirps)
        setChirps(updateFinalChirps)
    }
    return chirps.map((item, index) => {
        return <Chirp
            chirp={item}
            didRechirp={handleDidRechirp}
            className='my-5 py-5 border bg-white text-dark'
            key={`${index}-{item.id}`}/>
    })
}