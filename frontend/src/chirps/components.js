import React, {useEffect, useState} from 'react'

import {apiChirpAction, apiChirpCreate, apiChirpList} from './lookup'

export function ChirpsComponent(props) {
    const textAreaRef = React.createRef()
    const [newChirps, setNewChirps] = useState([])

    const handleBackendUpdate = (response, status) => {
        // backend api response handler
        let tempNewChirps = [...newChirps]
        if (status === 201) {
            tempNewChirps.unshift(response)
            setNewChirps(tempNewChirps)
        } else {
            console.log(response)
            alert("An error occured please try again")
        }
    }

    const handleSubmit = (event) => {
        event.preventDefault()
        const newVal = textAreaRef.current.value
        // backend api request
        apiChirpCreate(newVal, handleBackendUpdate)
        textAreaRef.current.value = ''
    }

    return <div className={props.className}>
        <div className='col-12 mb-3'>
            <form onSubmit={handleSubmit}>
                <textarea ref={textAreaRef} required={true} className='form-control' name='chirp'/>
                <button type='submit' className='btn btn-primary my-3'>Chirp</button>
            </form>
        </div>
        <ChirpsList newChirps={newChirps}/>
    </div>
}

export function ChirpsList(props) {
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
            apiChirpList(handleChirpListLookup)
        }
    }, [chirpsInit, chirpsDidSet, setChirpsDidSet])
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

export function ParentChirp(props) {
    const {chirp} = props
    return chirp.parent ? <div className='row'>
        <div className='col-11 mx-auto p-3 border rounded'>
            <p className='mb-0 text-muted small'>Rechirp</p>
            <Chirp hideActions className={' '} chirp={chirp.parent}/>
        </div>
    </div> : null
}

export function Chirp(props) {
    const {chirp, didRechirp, hideActions} = props
    const [actionChirp, setActionChirp] = useState(props.chirp ? props.chirp : null)
    const className = props.className ? props.className : 'col-10 mx-auto col-md-6'
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
        {(actionChirp && hideActions !== true) && <div className='btn btn-group'>
            <ActionBtn chirp={actionChirp} didPerformAction={handlePerformAction} action={{type: "chirp", display: "Chirp"}}/>
            <ActionBtn chirp={actionChirp} didPerformAction={handlePerformAction} action={{type: "unchirp", display: "Unchirp"}}/>
            <ActionBtn chirp={actionChirp} didPerformAction={handlePerformAction} action={{type: "rechirp", display: "Rechirp"}}/>
        </div>
        }
    </div>
}

export function ActionBtn(props) {
    const {chirp, action, didPerformAction} = props
    const [likes, setLikes] = useState(chirp.likes ? chirp.likes : 0)
    const className = props.className ? props.className : 'btn btn-primary btn-sm'
    const actionDisplay = action.display ? action.display : 'Action'

    const handleActionBackendEvent = (response, status) => {
        console.log(response, status)
        if ((status === 200 || status === 201) && didPerformAction) {
            didPerformAction(response, status)
        }
    }
    const handleClick = (event) => {
        event.preventDefault()
        apiChirpAction(chirp.id, action.type, handleActionBackendEvent)

    }
    const display = action.type === 'like' ? `${likes} ${actionDisplay}` : actionDisplay
    return <button className={className} onClick={handleClick}>{display}</button>
}
