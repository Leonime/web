import React, {useEffect, useState} from "react";
import {apiChirpList} from "./lookup";
import {Chirp} from "./detail";

function ChirpHandlersReturn(chirpsInit, setChirpsInit, chirps, setChirps, nextUrl, setNextUrl, props) {
    const handleDidRechirp = newChirp => {
        const updateChirpsInit = [...chirpsInit]
        updateChirpsInit.unshift(newChirp)
        setChirpsInit(updateChirpsInit)
        const updateFinalChirps = [...chirps]
        updateFinalChirps.unshift(chirps)
        setChirps(updateFinalChirps)
    }

    const handleLoadNext = (event) => {
        event.preventDefault()
        if (nextUrl !== null) {
            const handleLoadNextResponse = (response, status) => {
                if (status === 200) {
                    setNextUrl(response.next)
                    const newChirps = [...chirps].concat(response.results)
                    setChirpsInit(newChirps)
                    setChirps(newChirps)
                } else {
                    alert("There was an error")
                }
            }
            apiChirpList(props.username, handleLoadNextResponse, nextUrl)
        }
    }

    return <React.Fragment>{
        chirps.map((item, index) => {
            return <Chirp
                chirp={item}
                didRechirp={handleDidRechirp}
                className='mb-3 py-3 border border-dark rounded bg-secondary text-white'
                key={`${index}-{item.id}`}/>
        })
    }
        {nextUrl !== null && <button onClick={handleLoadNext} className='btn btn-outline-primary'>Load next</button>}
    </React.Fragment>
}

export function ChirpList(props) {
    const {front_page} = props
    const [chirpsInit, setChirpsInit] = useState([])
    const [chirps, setChirps] = useState([])
    const [nextUrl, setNextUrl] = useState(null)
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
                    setNextUrl(response.next)
                    setChirpsInit(response.results)
                    setChirpsDidSet(true)
                } else {
                    alert("There was an error")
                }
            }
            apiChirpList(props.username, handleChirpListLookup, null, front_page)
        }
    }, [chirpsInit, chirpsDidSet, setChirpsDidSet, props.username])

    return ChirpHandlersReturn(chirpsInit, setChirpsInit, chirps, setChirps, nextUrl, setNextUrl, props);
}

export function UserFeed(props) {
    const [chirpsDidSet, setChirpsDidSet] = useState(false)
    const [nextUrl, setNextUrl] = useState(null)
    const [chirpsInit, setChirpsInit] = useState([])
    const [chirps, setChirps] = useState([])

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
                    setNextUrl(response.next)
                    setChirpsInit(response.results)
                    setChirpsDidSet(true)
                } else {
                    alert("There was an error")
                }
            }
            apiChirpList(props.username, handleChirpListLookup, null)
        }
    }, [chirpsInit, chirpsDidSet, setChirpsDidSet, props.username])

    return ChirpHandlersReturn(chirpsInit, setChirpsInit, chirps, setChirps, nextUrl, setNextUrl, props);
}