import {backendLookup} from '../lookup'

export function apiChirpCreate(newChirp, callback) {
    backendLookup("POST", "chirps/", callback, {content: newChirp})
}

export function apiChirpList(username, callback) {
    let endpoint = "chirps/"
    if (username) {
        endpoint = `chirps/?username=${username}`
    }
    backendLookup("GET", endpoint, callback)
}

export function apiChirpDetail(chirpId, callback) {
    backendLookup("GET", `chirps/${chirpId}/`, callback)
}

export function apiChirpAction(chirp_id, action, callback) {
    const data = {id: chirp_id, action: action}
    backendLookup("POST", "chirps/" + chirp_id + "/like_action/", callback, data)
}
