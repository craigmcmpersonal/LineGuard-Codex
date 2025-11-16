import { LogLevel } from "@azure/msal-browser";

export const MICROSOFT_AUTHENTICATION_LIBRARY_CONFIGURATION = {
    auth: {
        clientId: import.meta.env.VITE_AUTHENTICATION_CLIENT_IDENTIFIER,
        authority: import.meta.env.VITE_AUTHENTICATION_AUTHORITY,
        redirectUri: window.location.origin,
        navigateToLoginRequestUrl: true,
    },
    cache: {
        cacheLocation: "sessionStorage",
        storeAuthStateInCookie: false,
    },
    system: {
        loggerOptions: {
            loggerCallback: (level, message, containsPii) => {
                if (containsPii) {
                    return;
                }
                switch (level) {
                    case LogLevel.Error:
                        console.error(message);
                        return;
                    case LogLevel.Info:
                        console.info(message);
                        return;
                    case LogLevel.Verbose:
                        console.debug(message);
                        return;
                    case LogLevel.Warning:
                        console.warn(message);
                        return;
                    default:
                        return;
                }
            },
        },
    },
};

export const loginRequest = {
    scopes: ['User.Read', "ProfilePhoto.Read.All"], //User.ReadWrite for photos maybe
};

