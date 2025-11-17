import "@/index.css"
import {createRoot} from "react-dom/client"
import "@/i18n.js";
import {App} from "@/App.jsx"
import {StrictMode} from "react"
import {PublicClientApplication} from '@azure/msal-browser';
import {MsalProvider} from '@azure/msal-react';
import {MICROSOFT_AUTHENTICATION_LIBRARY_CONFIGURATION} from '@/authenticationConfiguration.js';

const authenticator = new PublicClientApplication(
    MICROSOFT_AUTHENTICATION_LIBRARY_CONFIGURATION
);
await authenticator.initialize();

createRoot(document.getElementById("root")).render(
    <StrictMode>
        <MsalProvider instance={authenticator}>
            <App />
        </MsalProvider>
    </StrictMode>
)
