import {backendLookup} from '../lookup'

export function apiChirpCreate(newChirp, callback) {
    backendLookup("POST", "/api/v1/chipper/chirps/", callback, {content: newChirp})
}

export function apiChirpList(username, callback, nextUrl, front_page) {
    let endpoint = "/api/v1/chipper/chirps/"
    if (front_page) {
        endpoint = `/api/v1/chipper/chirps/feed/`
    }
    if (nextUrl !== null && nextUrl !== undefined) {
        endpoint = nextUrl
    }
    backendLookup("GET", endpoint, callback)
}

export function apiChirpDetail(chirpId, callback) {
    backendLookup("GET", `/api/v1/chipper/chirps/${chirpId}/`, callback)
}

export function apiChirpAction(chirp_id, action, callback) {
    const data = {id: chirp_id, action: action}
    backendLookup("POST", "/api/v1/chipper/chirps/" + chirp_id + "/like_action/", callback, data)
}
