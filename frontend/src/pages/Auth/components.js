import { Grid } from "@mui/material"
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns'
import { LocalizationProvider } from '@mui/x-date-pickers'


function AuthTemplate({content}) {
    return (
        <LocalizationProvider dateAdapter={AdapterDateFns}>
            <Grid container 
                position='relative' top={70}
                direction="row"
                justifyContent="center"
                alignItems="center"
                sx={{height: '90vh', mt: 1}}
                >
                <Grid item sx={{backgroundColor:"white"}}>
                    {content}
                </Grid>
            </Grid>
        </LocalizationProvider>
    )
}

export {AuthTemplate}