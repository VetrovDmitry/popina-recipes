import {configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/AuthSlice'

let store = configureStore({
    reducer: {
        auth: authReducer
    }
});

export default store;