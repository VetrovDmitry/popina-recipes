import { Outlet } from 'react-router-dom';
import {Header} from "./Header";
// import Footer from './Footer';

const Layout = ({props}) => {

    return (
        <>
            <Header props={props} />
            <div className="App" > 
                <Outlet />
            </div>
            {/* <Footer props={props} /> */}
        </>
    )
}

export {Layout}