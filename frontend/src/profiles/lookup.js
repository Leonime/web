import {backendLookup} from "../lookup";

export function apiProfileDetail(username, callback) {
    backendLookup("GET", `/api/v1/profiles/profile/profile/${username}/`, callback)
}