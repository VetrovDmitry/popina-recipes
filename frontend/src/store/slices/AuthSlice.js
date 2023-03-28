import { createSlice } from '@reduxjs/toolkit'
import decodeJWT from '../../hoc/AuthProvider';

const authSlice = createSlice({
    name: 'auth',
    initialState: { isAuthed: false, userId: null, username: null, avatarId: null},
    reducers: {
        loadIn: state => {
            const token = localStorage.getItem('accessToken')
            const [ , userId, username] = decodeJWT(token)
            state.userId = userId
            state.username = username
            state.isAuthed = true
        },
        loadOut: state => {
            state.userId = null
            state.username = null
            state.isAuthed = false
            localStorage.removeItem('accessToken')
        },
        scan: state => {
            return state.userId
        }
    } 
})

export const { loadIn, loadOut, scan } = authSlice.actions
export default authSlice.reducer