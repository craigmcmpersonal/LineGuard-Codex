import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger
} from "@/components/ui/dropdown-menu.jsx";
import {Button} from "@/components/ui/button.jsx";
import {UserRound} from "lucide-react";
import {
    LABEL_DELETE_ACCOUNT,
    LABEL_PROFILE_MENU,
    LABEL_RESET_PASSWORD,
    LABEL_SIGN_IN,
    LABEL_SIGN_OUT,
    LABEL_UPDATE_PROFILE
} from "@/lib/constants.js";
import {useMsal} from "@azure/msal-react";
import React from "react";
import {log} from "@/lib/utilities.js";

export const ProfileMenu = () => {
    const { instance: authenticator } = useMsal();

    const onAuthentication = () => {
        const accounts = authenticator.getAllAccounts();
        if (accounts.length > 0) {
            authenticator.setActiveAccount(accounts[0]);
        }
    };

    const onDeleteAccount = () => {
    };

    const onEditProfile = () => {
    };

    const onResetPassword = () => onSigningIn();

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
        <>
            <DropdownMenu>
                <DropdownMenuTrigger asChild>
                    <Button
                        variant="outline"
                        size="icon"
                        disabled={!activeAccount
                    }>
                        <UserRound
                            style={{ color: "#0FB7A6" }}
                            role="img"
                            aria-label={LABEL_PROFILE_MENU}
                        />
                    </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent className="w-56" align="start">
                    <DropdownMenuItem onClick={onResetPassword}>
                        {LABEL_RESET_PASSWORD}
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={onEditProfile}>
                        {LABEL_UPDATE_PROFILE}
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={onDeleteAccount}>
                        {LABEL_DELETE_ACCOUNT}
                    </DropdownMenuItem>
                </DropdownMenuContent>
            </DropdownMenu>
            <Button
                variant="outline"
                size="sm"
                className="hidden md:inline-flex border-[#0FB7A6]"
                onClick={
                activeAccount
                    ? onSigningOut
                    : onSigningIn
            }>
                {
                    activeAccount
                        ? LABEL_SIGN_OUT
                        : LABEL_SIGN_IN
                }
            </Button>
        </>
    )
}