import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { Provider } from 'react-redux'
import { CookiesProvider } from 'react-cookie'

import App from './App'
import store from './store/store';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <Provider store={store}>
      <BrowserRouter>
        <CookiesProvider>
            <App />
        </CookiesProvider>
      </BrowserRouter>
    </Provider>
);


