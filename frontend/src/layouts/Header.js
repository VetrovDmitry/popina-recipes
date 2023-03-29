import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom'
import { connect, useDispatch, useSelector } from 'react-redux';
import AppBar from '@mui/material/AppBar'
import Toolbar from '@mui/material/Toolbar'
import Typography from '@mui/material/Typography'
import { Link } from '@mui/material'

import { useAuth } from '../hook/useAuth';
import { loadOut } from '../store/slices/AuthSlice';


function Header(props) {

    const isAuthed = useSelector(state => state.auth.isAuthed)

    const dispatch = useDispatch()
    const navigate = useNavigate()

    return( 
        <header>
            <AppBar position="fixed">
            <Toolbar>
                <Typography variant="h6" component="div" sx={{ flexGrow: 1 }} onClick={() => navigate('/recipes')}>
                    Popina`s recipes
                </Typography>
                {(isAuthed ? <Link variant="h6" sx={{ mx: 1, color: 'white'}} onClick={() => dispatch(loadOut())}>Log out</Link> : <>
                    <Link variant="h6" sx={{ mx: 1, color: 'white'}} onClick={() => navigate('/login')}>Log in</Link>
                    <Link variant="h6" sx={{ mx: 1, color: 'white'}} onClick={() => navigate('/signup')}>Sign up</Link>
                </>)}
            </Toolbar>
            </AppBar>
        </header>
    )
}

export {Header}

const mapStateToProps = state => (
    {
      isAuthed: state.auth.isAuthed,
      userId: state.auth.userId,
    }
  )
  
  export default connect(
    mapStateToProps,
    {}
  )(Header)