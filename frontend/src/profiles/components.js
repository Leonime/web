import React from 'react'

export function UserLink(props) {
    const {username} = props
    const handleUserLink = (event) => {
        window.location.href = `/frontend/${username}/profile/`
    }
    return <span className='pointer' onClick={handleUserLink}>
      {props.children}
  </span>
}

export function UserDisplay(props) {
    const {user, hideLink} = props
    return <React.Fragment>
        {hideLink === true ? `@${user.username}` : <UserLink username={user.username}>@{user.username}</UserLink>}
    </React.Fragment>
}

export function UserPicture(props) {
    const {user, hideLink} = props
    const userIdSpan = <span className='mx-1 px-3 py-2 rounded-circle bg-dark text-white'>
  {user.username[0]}
</span>
    return hideLink === true ? userIdSpan : <UserLink username={user.username}>{userIdSpan}</UserLink>
}

export function ProfilePicture(props) {
    const {user} = props
    return user.image ? <img className="cover rounded-circle" src={user.image} alt={'Profile picture'}/>
    : <span className='mx-1 px-3 py-2 rounded-circle bg-dark text-white'>{user.username[0]}</span>
}

export function ProfileUser(props) {
    const {user} = props
    const nameDisplay = `${user.first_name} ${user.last_name}`
    return <div className="d-flex flex-column p-1 v-center">
        @{user.username}
        <span className="small text-muted">{nameDisplay}</span>
    </div>
}

