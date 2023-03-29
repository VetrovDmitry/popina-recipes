import { useState, useEffect } from "react"
import { useForm, Controller } from 'react-hook-form'
import * as Yup from 'yup'
import { yupResolver } from '@hookform/resolvers/yup'
import { Box, Card, CardContent, Avatar, Stack, Typography, List, Button, Divider, Link, Toolbar, 
    Tooltip, Dialog, DialogTitle, TextField, MenuItem, Select, InputLabel } from "@mui/material"
import { getRecipes, getUser, getUsers, postRecipe } from "../../middleware/api"


function MaxProfileCard({userId}) {
    const [username, setUsername] = useState("username")
    const [fullname, setFullname] = useState("Full name")
    const [email, setEmail] = useState("example@mail.com")

    useEffect(() => {
        async function fetchData() {
            try {
                const {data, code} = await getUser(userId)
                if (code === 200) {
                    setUsername(data.username)
                    setFullname(data.fullname)
                    setEmail(data.email)
                }
            } catch(error) {
                alert(error)
            }
        }
        (userId) && fetchData()
    }, [userId]);

    return (
        <Card sx={{ display: 'flex', boxShadow: 2}}>
            <Avatar variant="square" sx={{height: 150, width: 150, bgcolor: 'orange'}}>
                {username}
            </Avatar>
            <Box sx={{ display: 'flex', flexDirection: 'column'}}>
                <CardContent>
                    <Stack py={1}>
                        <Typography variant="h6">
                            {fullname}
                        </Typography>
                        <Typography variant="h6">
                            @{username}
                        </Typography>
                        <Typography>
                            {email}
                        </Typography>
                    </Stack>
                </CardContent>
            </Box>
        </Card>
    )
} 

export {MaxProfileCard}

const MinProfileCard = ({user}) => {

    return (
        <Card sx={{ display: 'flex', boxShadow: 2, mb: 1}}>
            <Avatar variant="square" sx={{height: 100, width: 100, bgcolor: 'lightgreen'}}>
                {user.username}
            </Avatar>
            <Box sx={{ display: 'flex', flexDirection: 'column'}}>
                <CardContent >
                    <Stack>
                        <Typography variant="subtitle1">
                            {user.fullname}
                        </Typography>
                        <Typography variant="subtitle1">
                            @{user.username}
                        </Typography>
                    </Stack>
                </CardContent>
            </Box>
        </Card>
    )
}

function MinProfileCardList({userId}) {
    const [users, setUsers] = useState([{id: 0, fullname: 'Full name', username: 'username'}])

    useEffect(() => {
        async function fetchData() {
            try {
                const {data, code} = await getUsers()
                if (code === 200) {
                    setUsers(data.users)
                }
            } catch(error) {
                alert(error)
            }
        }
        userId && fetchData()  
    }, [userId]);
    
    return (
        <List>
            {users.map(user => user.id !== userId && <MinProfileCard key={user.id} user={user}/>)}
        </List>
    )
}

export {MinProfileCardList}

const recipeSchema = Yup.object().shape({
    title: Yup.string()
        .required('field is required')
        .min(1)
        .max(80)
        .matches(/^[a-z0-9_,.\s]+$/i, "Only alphabets and numbers are allowed for this field"),
    description: Yup.string()
        .required('field is required')
        .matches(/^[a-z0-9_,.\s]+$/i, "Only alphabets and numbers are allowed for this field"),
    complexity: Yup.string()
        .required('field is required')
        .oneOf(['easy', 'medium', 'hard']),
    cookingTime: Yup.number()
        .required('field is required'),
    instruction: Yup.string()
        .required('field is required')
})

const RecipeForm = ({onUpdate, setOpen}) => {

    const { handleSubmit, control, reset } = useForm({
        resolver: yupResolver(recipeSchema),
        mode: "onChange"
    })

    async function onSubmit(data) {
        const title = data.title
        const description = data.description
        const complexity = data.complexity
        const cookingTime = data.cookingTime
        const instruction = data.instruction
        try {
            const {data, code} = await postRecipe(
                title,
                description, 
                complexity, 
                cookingTime, 
                instruction, 
            )
            if (code === 201) {
                onUpdate(true)
                setOpen(false)
                console.log(data)
            }
            console.log(2222)
        } catch(error) {
            alert(error.response.data.message)
        }
    }

    return (
        <form onSubmit={handleSubmit(onSubmit)}>
            <Controller
                name="complexity"
                control={control}
                render={({ field: { onChange, value }, fieldState: { error } }) => (
                    <>
                        <InputLabel>Complexity</InputLabel>
                        <Select
                            variant="filled"
                            fullWidth
                            label="complexity"
                            defaultValue=""
                            value={value ? value: ""}
                            onChange={onChange}
                            error={!!error}
                            helpertext={error ? error.message : null}>
                            <MenuItem value="easy">easy</MenuItem>
                            <MenuItem value="medium">medium</MenuItem>
                            <MenuItem value="hard">hard</MenuItem>
                        </Select>
                    </>
                )}
            />
            <Controller 
                name="cookingTime"
                control={control}
                defaultValue=""
                render={({ field: { onChange, value }, fieldState: { error } }) => (
                    <TextField
                        variant="filled"
                        fullWidth
                        sx={{mt: 1}}
                        label="Cooking Time(minutes)"
                        value={value}
                        onChange={onChange}
                        error={!!error}
                        helperText={error ? error.message : null}
                    />
                )}
            />
            <Controller 
                name="title"
                control={control}
                defaultValue=""
                render={({ field: { onChange, value }, fieldState: { error } }) => (
                    <TextField
                        variant="filled"
                        fullWidth
                        sx={{mt: 1}}
                        label="Title"
                        value={value}
                        onChange={onChange}
                        error={!!error}
                        helperText={error ? error.message : null}
                    />
                )}
            />
            <Controller 
                name="description"
                control={control}
                defaultValue=""
                render={({ field: { onChange, value }, fieldState: { error } }) => (
                    <TextField
                        variant="filled"
                        fullWidth
                        sx={{mt: 1}}
                        label="Description"
                        value={value}
                        onChange={onChange}
                        error={!!error}
                        helperText={error ? error.message : null}
                        multiline    
                    />
                )}
            />
            <Controller 
                name="instruction"
                control={control}
                defaultValue=""
                render={({ field: { onChange, value }, fieldState: { error } }) => (
                    <TextField
                        variant="filled"
                        fullWidth
                        sx={{my: 1, mb: 2}}
                        label="Instruction"
                        value={value}
                        onChange={onChange}
                        error={!!error}
                        helperText={error ? error.message : null}
                        multiline    
                    />
                )}
            />
            <Button fullWidth type="submit" variant="contained" color="primary" sx={{my: 2}}>Publish</Button>
        </form>
    )

}

const RecipeDialog = ({open, setOpen, onUpdate}) => {
    return (
        <Dialog onClose={() => setOpen(false)} open={open}>
            <DialogTitle align="center">Create recipe</DialogTitle>
            <Box width={400} px={2}>
                <RecipeForm onUpdate={onUpdate} setOpen={setOpen} />
            </Box>
        </Dialog>
    )
}

const AddRecipeCard = ({onUpdate}) => {
    const [open, setOpen] = useState(false)

    return (
        <Card>
            <CardContent>
                <Link underline="hover" variant="h6" mx={1} onClick={() => setOpen(true)}>
                    Add recipe
                </Link>
            </CardContent>
            <RecipeDialog open={open} setOpen={setOpen} onUpdate={onUpdate}/>
        </Card>
    )
}

const RecipeDetails = ({description, instruction}) => {
    return (
        <Box>
            <Typography variant="subtitle1">
                {description}
            </Typography>
            <Divider />
            <Typography>
                {instruction}
            </Typography>
        </Box>
    )
}

const RecipeCard = ({recipe}) => {
    const colors = {
        "easy": 'green',
        "medium": 'orange',
        "hard": 'red'
    }
    return (
        <Tooltip arrow title={<RecipeDetails description={recipe.description} instruction={recipe.instruction} />}>
            <Card sx={{ display: 'flex', boxShadow: 2, mb: 1}}>
                <Avatar variant="square" sx={{height: 100, width: 100, bgcolor: 'lightgrey'}}>
                    recipe
                </Avatar>
                <Box sx={{ display: 'flex', flexDirection: 'row', py: 1}}>
                    <CardContent  direction="row" spacing={2} sx={{overflow: "hidden", textOverflow: "ellipsis"}} >
                        <Typography noWrap display='inline-block' variant="h6" mx={1}>
                            {recipe.title}
                        </Typography>
                        <Typography noWrap display='inline-block' variant="h6" mx={1} maxWidth={450}>
                            {recipe.description}
                        </Typography>
                        <Typography noWrap display='inline-block' variant="h6" color="grey" mx={1}>
                            {recipe.cooking_time} min
                        </Typography>
                        <Typography noWrap display='inline-block' variant="h6" mx={1} color={colors[recipe.complexity]}>
                            {recipe.complexity}
                        </Typography>   
                    </CardContent>
                </Box>    
            </Card>
        </Tooltip>
    )
}

function RecipeBlock() {
    const [updated, setUpdated] = useState(true)
    const [recipes, setRecipes] = useState([{
        id: 0, 
        title: 'Title', 
        description: 'Description',
        cooking_time: 0, 
        complexity: 'easy'
    }])

    useEffect(() => {
        async function fetchData() {
            try {
                const {data, code} = await getRecipes()
                if (code === 200) {
                    setRecipes(data.recipes)
                    setUpdated(false)
                }
            } catch(error) {
                alert(error)
            }
        }
        updated && fetchData()  
    }, [updated]);

    return (<>
        <AddRecipeCard onUpdate={setUpdated} />
        <List> 
            {recipes.map(recipe => <RecipeCard key={recipe.id} recipe={recipe} />)}
        </List>
    </>)

}

export {RecipeBlock}
