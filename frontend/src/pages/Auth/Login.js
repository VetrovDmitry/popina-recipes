import { useEffect } from "react"
import { useNavigate } from 'react-router-dom'
import { connect, useDispatch } from "react-redux"
import { useForm, Controller } from 'react-hook-form'
import * as Yup from 'yup'
import { yupResolver } from '@hookform/resolvers/yup'
import { Container } from '@mui/system'
import { Button, TextField, Typography, FormControl, Box, Link } from '@mui/material'

import { loadIn } from "../../store/slices/AuthSlice"
import { token } from '../../middleware/api'
import { useAuth }  from '../../hook/useAuth'
import { AuthTemplate } from "./components"

const loginSchema = Yup.object().shape({
    username: Yup.string()
        .required('field is required')
        .min(1)
        .max(50)
        .matches(/^[a-z0-9_]+$/i, "Only alphabets and numbers are allowed for this field"),
    password: Yup.string()
        .required('field is requiered')
        .min(7)
        .max(50)
        .matches(/^[A-Za-z0-9]+$/i, "Only characters and numbers required for this field"),
})

const LoginForm = (props) => {

    const navigate = useNavigate()
    const { signIn, isAuthenticated } = useAuth() 
    const { handleSubmit, control } = useForm({
        resolver: yupResolver(loginSchema),
        mode: "onChange"
    })


    useEffect(() => {
        if (isAuthenticated()) { 
            navigate("/recipes")
        }
    }, [])

    async function onSubmit(data) {
        const username = data.username;
        const password = data.password;
        try {
            const {data, code} = await token(username, password)
            if (code === 202) {
                signIn(data['access_token'])
                navigate('/recipes')
            }
        } catch(error) {
            alert(error)
        }
    }
    
    return (
        <form onSubmit={handleSubmit(onSubmit)}>
            <Controller
                name="username"
                control={control}
                defaultValue=""
                render={({ field: { onChange, value }, fieldState: { error } }) => (
                    <TextField
                        variant="filled"
                        fullWidth
                        sx={{mt: 1}}
                        label="Username"
                        value={value}
                        onChange={onChange}
                        error={!!error}
                        helperText={error ? error.message : null}
                    />
                )}
            />
            <Controller
                name="password"
                control={control}
                defaultValue=""
                render={({ field: { onChange, value }, fieldState: { error } }) => (
                    <TextField
                        label="Password"
                        variant="filled"
                        fullWidth
                        sx={{mt: 1}}
                        value={value}
                        onChange={onChange}
                        error={!!error}
                        helperText={error ? error.message : null}
                        type="password"
                    />
                )}
            />
            <Button fullWidth type="submit" variant="contained" color="primary" sx={{my: 2}} >Send</Button>
        </form>
    )
};

function LoginPage(props) {
  
    return (
        <AuthTemplate
            content={
                <Container sx={{
                    width: 380,
                    p: 4,
                    boxShadow: 2}}
                >
                    <Typography variant='h5' align='center' color={'primary.light'}>Authorization</Typography>
                    <FormControl>          
                        <LoginForm props={props}/>
                    </FormControl>
                </Container>
            
            }
        />
    )
}

const mapStateToProps = state => {
    return {
        isAuthed: state.auth.isAuthed
    }
}

const mapDispatchToProps = dispatch => {
    return {
        loadIn: () => dispatch(loadIn())
    }
}

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(LoginPage)