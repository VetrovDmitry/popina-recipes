import { useSelector } from 'react-redux' 
import { Grid } from "@mui/material" 
import { MaxProfileCard, MinProfileCardList, RecipeBlock } from "./components"

function RecipePage() {
    const userId = useSelector(state => state.auth.userId)
    return(
        <Grid container
            direction="row"
            justifyContent="center"
            alignItems="flex-start"
            mt={10}
        >
            <Grid item
                m={1}
                width={400}
            >
                <MaxProfileCard userId={userId} />
                <MinProfileCardList userId={userId} />
            </Grid>
            <Grid item
                m={1}
                width={800}
            >
                <RecipeBlock />
            </Grid>

        </Grid>
    )
}

export {RecipePage}