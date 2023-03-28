

const NotAuthedHeader = () => {
    return (
        <header>
            this is not authed header
        </header>
    )
}

const AuthedHeader = () => {
    return (
        <header>
            this is authed header
        </header>
    )
}

function Header() {
    return <NotAuthedHeader />
}

export {Header}