

import React from "react"
import { createContext } from "react"
import jwtDecode from "jwt-decode"
import { refreshToken } from "../middleware/api"

export const AuthContext = createContext(null)

const decodeJWT = (token) => {
    const decodedToken = jwtDecode(token)
    const user = JSON.parse(decodedToken.sub.replaceAll("'", '"'))
    return [decodedToken.exp, user.id, user.username]
}

export default decodeJWT

export const AuthProvider = ({children}) => {
    const signIn = (accessToken) => {
        localStorage.setItem('accessToken', accessToken)
    }
    const signOut = () => {
        localStorage.removeItem('accessToken')
    }
    const signUpdate = async () => {
        try {
            const {data, code} = await refreshToken()
            signIn(data['access_token'])
        } catch(error) {
            signOut()
        }
    }
    const checkAccess = () => {
        var nowUtc = new Date().toUTCString()
        var nowSeconds = Date.parse(nowUtc) / 1000
        const token = localStorage.getItem('accessToken')
        if (token) {
            const [expires,] = decodeJWT(token)
            if (nowSeconds > expires) {
                signOut()
                return false
            }
            if (nowSeconds + 30 > expires) {
                signUpdate()
            }
            return true
        }
        return false
    }
    const isAuthenticated = () => {
        const token = localStorage.getItem('accessToken')
        if (token) {
            const [ , userId, username] = decodeJWT(token)
            if (!userId || !username){
                signOut()
                return false
            }
            return true
        }
        return false
    }
    const value = {signIn, signOut, signUpdate, isAuthenticated, checkAccess}
    return <AuthContext.Provider value={value}>
        {children}
    </AuthContext.Provider>
}