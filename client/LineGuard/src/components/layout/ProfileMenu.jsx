import { useTranslation } from "react-i18next";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger
} from "@/components/ui/dropdown-menu.jsx";
import {Button} from "@/components/ui/button.jsx";
import {UserRound} from "lucide-react";
import {useMsal} from "@azure/msal-react";
import React from "react";
import {log} from "@/lib/utilities.js";
import {TooltipProvider, Tooltip, TooltipContent} from "@/components/ui/tooltip.jsx";
import {TooltipTrigger} from "@radix-ui/react-tooltip";
import {AuthenticationButton} from "@/components/ui/AuthenticationButton.jsx";

export const ProfileMenu = ({ state, dispatchState, reference}) => {
    const { t:translate } = useTranslation("common");
    const { instance: authenticator } = useMsal();

    const onDeleteAccount = () => {
    };

    const onEditProfile = () => {
    };

    const onResetPassword = () => authenticator.loginPopup();

    const activeAccount = authenticator.getActiveAccount();
    log(activeAccount);

    return (
        <>
            <TooltipProvider>
                <DropdownMenu>
                    <Tooltip>
                        <TooltipTrigger asChild>
                            <DropdownMenuTrigger asChild>
                                <Button
                                    variant="outline"
                                    size="icon"
                                    disabled={!activeAccount
                                }>
                                    <UserRound
                                        style={{ color: "#0FB7A6" }}
                                        role="img"
                                        aria-label={translate("LABEL_PROFILE_MENU")}
                                    />
                                </Button>
                            </DropdownMenuTrigger>
                        </TooltipTrigger>
                        <TooltipContent side="bottom">
                            {translate("LABEL_PROFILE_MENU")}
                        </TooltipContent>
                    </Tooltip>
                    <DropdownMenuContent className="w-56" align="start">
                        <DropdownMenuItem onClick={onResetPassword}>
                            {translate("LABEL_RESET_PASSWORD")}
                        </DropdownMenuItem>
                        <DropdownMenuItem onClick={onEditProfile}>
                            {translate("LABEL_UPDATE_PROFILE")}
                        </DropdownMenuItem>
                        <DropdownMenuItem onClick={onDeleteAccount}>
                            {translate("LABEL_DELETE_ACCOUNT")}
                        </DropdownMenuItem>
                    </DropdownMenuContent>
                </DropdownMenu>
            </TooltipProvider>
            <AuthenticationButton
                state={state}
                dispatchState={dispatchState}
                reference={reference}
                variant="outline"
                size="sm"
                label={translate("LABEL_SIGN_IN")}
                className="hidden md:inline-flex border-[#0FB7A6]"
            />
        </>
    )
};