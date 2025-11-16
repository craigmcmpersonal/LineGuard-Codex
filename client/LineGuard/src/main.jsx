import {createRoot} from "react-dom/client"
import {App} from "@/App.jsx"
import {BrowserRouter} from "react-router-dom"
import {StrictMode} from "react"
import "@/index.css"
import { PublicClientApplication, EventType } from '@azure/msal-browser';
import { MsalProvider } from '@azure/msal-react';
import { MICROSOFT_AUTHENTICATION_LIBRARY_CONFIGURATION } from '@/authenticationConfiguration.js';

const authenticator = new PublicClientApplication(
    MICROSOFT_AUTHENTICATION_LIBRARY_CONFIGURATION
);
await authenticator.initialize();

createRoot(document.getElementById("root")).render(
    <StrictMode>
        <MsalProvider instance={authenticator}>
            <BrowserRouter>
                <App />
            </BrowserRouter>
        </MsalProvider>
    </StrictMode>
)
