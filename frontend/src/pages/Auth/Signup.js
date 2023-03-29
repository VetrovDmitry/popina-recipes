import { useEffect } from "react"
import { useNavigate } from 'react-router-dom'
import { useForm, Controller } from 'react-hook-form'
import * as Yup from 'yup'
import { yupResolver } from '@hookform/resolvers/yup'
import { Container } from '@mui/system'
import { Button, TextField, Typography, Box, FormControl } from '@mui/material'
import { MenuItem, Select, Alert, InputLabel, Link } from '@mui/material'

import { postUser } from '../../middleware/api'
import { useAuth }  from '../../hook/useAuth'
import { AuthTemplate } from "./components"


const registerSchema = Yup.object().shape({
    firstName: Yup.string()
        .required('field is required')
        .min(1)
        .max(50)
        .matches(/^[aA-zZ]+$/, "only alphabets are allowed for this field"),
    lastName: Yup.string()
        .required('field is required')
        .min(1)
        .max(50)
        .matches(/^[aA-zZ]+$/, "Only alphabets are allowed for this field"),
    username: Yup.string()
        .required('field is required')
        .min(1)
        .max(50)
        .matches(/^[a-z0-9_]+$/i, "Only alphabets and numbers are allowed for this field"),
    sex: Yup.string()
        .required('field is required')
        .oneOf(['male', 'female']),
    birthDate: Yup.string()
        .required('field is required')
        ,
    email: Yup.string().email()
        .required('field is requiered')
        .matches(/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i, "not valid symbols"),
    password: Yup.string()
        .required('field is requiered')
        .min(7)
        .max(50)
        .matches(/^[A-Za-z0-9]+$/i, "Only characters and numbers required for this field"),
    confirmPassword: Yup.string()
        .required('field is requiered')
        .oneOf([Yup.ref('password'), null], 'passwords must match'),
})


const RegisterForm = ({callback}) => {

    const navigate = useNavigate()

    const { isAuthenticated } = useAuth() 

    useEffect(() => {
        if (isAuthenticated()) { 
            navigate("/recipes")
        }
    }, [])

    const { handleSubmit, control, reset } = useForm({
        resolver: yupResolver(registerSchema),
        mode: "onChange"
    })

    async function onSubmit(data) {
        const firstName = data.firstName
        const lastName = data.lastName
        const username = data.username
        const sex = data.sex
        const birthDate = data.birthDate
        const email = data.email
        const password = data.password
        try {
            const {data, code} = await postUser(
                firstName,
                lastName, 
                username, 
                sex, 
                birthDate, 
                email,
                password
            )
            if (code === 201) {
                alert(`Registred succesed as @${username}!`)
                return callback('/login')
            }
        } catch(error) {
            alert(error.response.data.message)
        }
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)}>
            <Controller
                name="sex"
                control={control}
                render={({ field: { onChange, value }, fieldState: { error } }) => (
                    <>
                        <InputLabel>Sex</InputLabel>
                        <Select
                            variant="filled"
                            fullWidth
                            label="sex"
                            defaultValue=""
                            value={value ? value: ""}
                            onChange={onChange}
                            error={!!error}
                            helpertext={error ? error.message : null}>
                            <MenuItem value="male">male</MenuItem>
                            <MenuItem value="female">female</MenuItem>
                        </Select>
                    </>
                )}
            />
            <Controller
                name="birthDate"
                control={control}
                render={({ field: { onChange, value }, fieldState: { error } }) => (
                    <TextField
                        id="date"
                        label="Birth Date"
                        type="date"
                        variant="filled"
                        fullWidth
                        sx={{mt: 1}}
                        value={value ? value: ""}
                        onChange={onChange}
                        error={!!error}
                        helperText={error ? error.message : null}
                        InputLabelProps={{
                            shrink: true,
                        }}
                    />
                )}
                rules={{ 
                    required: 'Field should be filled', 
                }}
            />
            <Controller
                name="firstName"
                control={control}
                defaultValue=""
                render={({ field: { onChange, value }, fieldState: { error } }) => (
                    <TextField
                        variant="filled"
                        fullWidth
                        sx={{mt: 1}}
                        label="First Name"
                        value={value}
                        onChange={onChange}
                        error={!!error}
                        helperText={error ? error.message : null}
                    />
                )}
            />
            <Controller
                name="lastName"
                control={control}
                defaultValue=""
                render={({ field: { onChange, value }, fieldState: { error } }) => (
                    <TextField
                        variant="filled"
                        fullWidth
                        sx={{mt: 1}}
                        label="Last Name"
                        value={value}
                        onChange={onChange}
                        error={!!error}
                        helperText={error ? error.message : null}
                    />
                )}
            />
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
                name="email"
                control={control}
                defaultValue=""
                render={({ field: { onChange, value }, fieldState: { error } }) => (
                    <TextField
                        label="E-mail"
                        variant="filled"
                        fullWidth
                        sx={{mt: 1}}
                        value={value}
                        onChange={onChange}
                        error={!!error}
                        helperText={error ? error.message : null}
                        type="email"
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
            <Controller
                name="confirmPassword"
                control={control}
                defaultValue=""
                render={({ field: { onChange, value }, fieldState: { error } }) => (
                    <TextField
                        label="Confirm Password"
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
            <Box sx={{mt: 4}}>
                <Button 
                    type="button" 
                    variant="text"
                    onClick={() => {
                        reset({
                            firstName: "",
                            lastName: "",
                            birthDate: ""
                        });
                      }}  >
                    Clear
                </Button>
                <Button type="submit" variant="contained" color="primary" sx={{ml: 24}}>
                    Send
                </Button>
            </Box>
        </form>
    )
}

function SignupPage() {
    const navigate = useNavigate()
    return (
        <AuthTemplate
            content={
                <Container sx={{
                    width: 380,
                    p: 4
                }}
                >
                    <Typography variant='h5' align='center' color={'primary.light'}>Registration</Typography>
                    <FormControl>          
                        <RegisterForm callback={navigate}/>
                    </FormControl>
                </Container>
            }
        />
    )
}

export {SignupPage}