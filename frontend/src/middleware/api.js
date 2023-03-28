import axios from 'axios'

const HEADERS = {
    'accept': 'application/json',
    'X-API-Key': process.env.REACT_APP_API_KEY,
    'Content-Type': 'multipart/form-data',
    'Access-Control-Allow-Origin' : '*',
}
const api = axios.create({
    withCredentials: true,
    baseURL: process.env.REACT_APP_API_URL,
    headers: HEADERS,
})

async function postUser(firstName, lastName, username, passcode, sex, birthDate, email, password) {
    const formData = {
        first_name: firstName,
        last_name: lastName,
        username: username,
        passcode: passcode,
        sex: sex,
        birth_date: birthDate,
        email: email,
        password: password
    }
    const response =  await api.post('/signup', formData)
    const data =  await response.data
    const code = response.status
    return {data, code}
}

export {postUser}

async function putUser(userId, username, email, password) {
    const formData = {
        user_id: userId,
        username: username,
        email: email,
        password: password 
    }
    const response = await api.put('/user', formData)
    const code = response.status
    return code
}

export {putUser}

async function getUser(userId, username, email, password) {
    const formData = {
        user_id: userId,
        username: username,
        email: email,
        password: password 
    }
    const response = await api.get('/user', formData)
    const code = response.status
    return code
}

export {getUser}

async function token(username, password) {
    const formData = {
        username: username,
        password: password
    }
    const response = await api.post('/token', formData)
    const data = response.data
    const code = response.status
    api.defaults.headers.common['X-AUTH-Key'] = data['access_token']
    return {data, code}
}

export {token}

async function refreshToken() {
    api.defaults.headers.common['X-AUTH-Key'] = localStorage.getItem('accessToken')
    const response = await api.patch('/refresh-token')
    const data = response.data
    const code = response.status
    api.defaults.headers.common['X-AUTH-Key'] = data['access_token']
    return {data, code}
}

export {refreshToken}