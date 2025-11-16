import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger
} from "@/components/ui/dropdown-menu.jsx";
import {Tooltip, TooltipContent, TooltipProvider, TooltipTrigger} from "@/components/ui/tooltip.jsx";
import {Button} from "@/components/ui/button.jsx";
import {UserRound} from "lucide-react";
import {LABEL_SIGN_IN, LABEL_SIGN_OUT} from "@/lib/constants.js";
import {AuthenticatedTemplate, UnauthenticatedTemplate, useMsal} from "@azure/msal-react";
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
        <TooltipProvider>
            <DropdownMenu>
                <Tooltip>
                    <TooltipTrigger asChild>
                        <DropdownMenuTrigger asChild>
                            <Button variant="outline" size="icon">
                                <UserRound
                                    style={{ color: "#0FB7A6" }}
                                    role="img"
                                    aria-label={activeAccount
                                        ? LABEL_SIGN_OUT
                                        : LABEL_SIGN_IN
                                    }
                                />
                            </Button>
                        </DropdownMenuTrigger>
                    </TooltipTrigger>
                    <TooltipContent side="bottom">
                        {activeAccount
                            ? LABEL_SIGN_OUT
                            : LABEL_SIGN_IN
                        }
                    </TooltipContent>
                </Tooltip>
                <DropdownMenuContent className="w-56" align="start">
                    <AuthenticatedTemplate>
                        <DropdownMenuItem onClick={onSigningOut}>
                            {LABEL_SIGN_OUT}
                        </DropdownMenuItem>
                    </AuthenticatedTemplate>
                    <UnauthenticatedTemplate>
                        <DropdownMenuItem onClick={onSigningIn}>
                            {LABEL_SIGN_IN}
                        </DropdownMenuItem>
                    </UnauthenticatedTemplate>
                </DropdownMenuContent>
            </DropdownMenu>
        </TooltipProvider>
    )
}