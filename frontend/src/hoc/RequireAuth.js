import React, { useState, useEffect} from "react"
import { useSelector } from "react-redux"
import { useLocation, Navigate } from "react-router-dom"
import { useDispatch } from "react-redux"
import { loadIn, loadOut } from "../store/slices/AuthSlice"
import { useAuth } from "../hook/useAuth"


const RequireAuth = ({children}) => {
    const interval = 15
    const location = useLocation()
    const dispatch = useDispatch()
    const { isAuthenticated, checkAccess } = useAuth()
    const [seconds, setSeconds] = useState(interval)

    useEffect(() => {
        const timer = setInterval(() => {
            if (seconds > 0) {
                setSeconds(seconds - 1)
            }
            if (seconds === 0) {
                if (!checkAccess()) {
                    dispatch(loadOut())
                    return <Navigate to="/login" state={{from: location}} />
                }
                setSeconds(interval)
            }
        }, 1000)
        return () => clearInterval(timer)
    }, [seconds])

    if (!isAuthenticated()) {
        dispatch(loadOut())
        return <Navigate to="/login" state={{from: location}} />
    }

    dispatch(loadIn())
    return children
}

export {RequireAuth}