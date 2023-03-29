import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { AuthProvider } from './hoc/AuthProvider'
import { Layout } from './layouts/Main'
import HomePage from './pages/Main/Home'
import { NotfoundPage } from './pages/Notfound'
import LoginPage from './pages/Auth/Login'
import { SignupPage } from './pages/Auth/Signup'
import { RecipePage } from './pages/Main/Recipe'
import { RequireAuth } from './hoc/RequireAuth'


function App() {
  return (
    <AuthProvider>
       <Routes>
        <Route path='/' element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route path="*" element={<NotfoundPage />} />
          <Route path="/recipes" element={
            <RequireAuth>
                <RecipePage />
            </RequireAuth>
          } />
        </Route>
      </Routes>
    </AuthProvider>
   
  )
}

export default App
