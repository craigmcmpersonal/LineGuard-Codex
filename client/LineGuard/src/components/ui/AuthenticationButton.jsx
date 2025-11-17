import { useTranslation } from "react-i18next";
import {Button} from "@/components/ui/button.jsx";
import {useMsal} from "@azure/msal-react";
import React from "react";
import {log} from "@/lib/utilities.js";

export const AuthenticationButton = ({ state, dispatchState, reference, variant, size, label, className}) => {
    const { t:translate } = useTranslation("common");
    const { instance: authenticator } = useMsal();

    const onAuthentication = () => {
        const accounts = authenticator.getAllAccounts();
        if (accounts.length > 0) {
            authenticator.setActiveAccount(accounts[0]);
        }
    };

    const onSigningIn = () => {
        authenticator.loginPopup()
            .then(
                authenticationResult => {
                    authenticator.setActiveAccount(authenticationResult.account);
                }
            )
            .catch(
                exception => console.error(exception)
            );
    };

    const onSigningOut = () => {
        authenticator.logout().catch(
            exception => console.error(exception)
        );
    };

    React.useEffect(onAuthentication, [authenticator]);

    const activeAccount = authenticator.getActiveAccount();
    log(activeAccount);

    return (
        <Button
            variant={variant}
            size={size}
            className={className}
            onClick={
                activeAccount
                    ? onSigningOut
                    : onSigningIn
            }>
            {
                activeAccount
                    ? translate("LABEL_SIGN_OUT")
                    : label
            }
        </Button>
    )
};