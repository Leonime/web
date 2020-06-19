import {backendLookup} from '../lookup'

export function apiChirpCreate(newTweet, callback) {
    backendLookup("POST", "chirps/", callback, {content: newTweet})
}

export function apiChirpList(callback) {
    backendLookup("GET", "chirps/", callback)
}

export function apiChirpAction(chirp_id, action, callback) {
    const data = {id: chirp_id, action: action}
    backendLookup("POST", "chirps/" + chirp_id + "/like_action/", callback, data)
}