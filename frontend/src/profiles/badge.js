import React, {useEffect, useState} from 'react'
import ShowMore from 'react-show-more';


import {ProfileLocation, ProfilePicture, ProfileStats, ProfileUser, UserDisplay} from './components'
import {apiProfileDetail, apiProfileFollowToggle} from './lookup'
import {DisplayCount} from "./utils";


function SetProfile(props) {
    const {user, didFollowToggle, profileLoading} = props
    let currentVerb = (user && user.is_following) ? "Unfollow" : "Follow"
    currentVerb = profileLoading ? "Loading..." : currentVerb
    const handleFollowToggle = (event) => {
        event.preventDefault()
        if (didFollowToggle && !profileLoading) {
            didFollowToggle(currentVerb)
        }
    }
    return {user, currentVerb, handleFollowToggle};
}

function ProfileBadge(props) {
    let {user, currentVerb, handleFollowToggle} = SetProfile(props);
    return user ? <div>
        <p><UserDisplay user={user} includeFullName hideLink/></p>
        <p><DisplayCount>{user.follower_count}</DisplayCount> {user.follower_count === 1 ? "follower" : "followers"}
        </p>
        <p><DisplayCount>{user.following_count}</DisplayCount> following</p>
        <p>{user.location}</p>
        <p>{user.bio}</p>
        <button className='btn btn-primary' onClick={handleFollowToggle}>{currentVerb}</button>
    </div> : null
}

function Profile(props) {
    let {user, currentVerb, handleFollowToggle} = SetProfile(props);

    return user ? <div className="d-flex border border-rounded border-secondary">
        <div className="d-flex flex-row">
            <div className="d-flex p-1 v-center">
                <ProfilePicture user={user} />
            </div>
            <div className="d-flex">
                <ProfileUser user={user}/>
            </div>
            <div className="d-flex p-1 v-center">
                <button className='btn btn-sm btn-secondary' onClick={handleFollowToggle}>{currentVerb}</button>
            </div>
        </div>
        <div className="d-flex flex-fill flex-column border-left border-dark">
            <ProfileLocation location={user.location}/>
            <div className="p-1">
                <ShowMore
                    lines={1}
                    more='more'
                    less='less'
                    anchorClass='badge badge-secondary'
                >
                    {user.bio}
                </ShowMore>
            </div>
        </div>
        <div className="d-flex border-left border-dark">
            <ProfileStats number={user.chirp_count} display={'Chirp'}/>
            <ProfileStats number={user.follower_count} display={'Follower'}/>
            <ProfileStats number={user.following_count} display={'Following'}/>
        </div>
    </div> : null
}

function ProfileHandlers(props) {
    const {username} = props
    const [didLookup, setDidLookup] = useState(false)
    const [profile, setProfile] = useState(null)
    const [profileLoading, setProfileLoading] = useState(false)
    const handleBackendLookup = (response, status) => {
        if (status === 200) {
            setProfile(response)
        }
    }
    useEffect(() => {
        if (didLookup === false) {
            apiProfileDetail(username, handleBackendLookup)
            setDidLookup(true)
        }
    }, [username, didLookup, setDidLookup])

    const handleNewFollow = (actionVerb) => {
        apiProfileFollowToggle(username, actionVerb, (response, status) => {
            if (status === 200) {
                setProfile(response)
            }
            setProfileLoading(false)
        })
        setProfileLoading(true)

    }
    return {didLookup, profile, profileLoading, handleNewFollow};
}

export function ProfileBadgeComponent(props) {
    const {didLookup, profile, profileLoading, handleNewFollow} = ProfileHandlers(props);
    return didLookup === false ? "Loading..." : profile ?
        <ProfileBadge user={profile} didFollowToggle={handleNewFollow} profileLoading={profileLoading}/> : null
}

export function ProfileComponent(props) {
    const {didLookup, profile, profileLoading, handleNewFollow} = ProfileHandlers(props);
    return didLookup === false ? "Loading..." : profile ?
        <Profile user={profile} didFollowToggle={handleNewFollow} profileLoading={profileLoading}/> : null
}