import {backendLookup} from "../lookup";

export function apiProfileDetail(username, callback) {
    backendLookup("GET", `/api/v1/profiles/profile/profile/${username}/`, callback)
}

export function apiProfileFollowToggle(username, action, callback) {
    const data = {action: `${action && action}`.toLowerCase()}
    backendLookup("POST", `/api/v1/profiles/profile/follow/${username}/`, callback, data)
}
