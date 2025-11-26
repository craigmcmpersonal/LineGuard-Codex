import { useTranslation } from "react-i18next";
import {ACTION_ON_INITIATE_IMPORT} from "@/lib/state.js";
import {
    NavigationMenu,
    NavigationMenuList,
} from "@/components/ui/navigation-menu.jsx"

import {
    Sheet,
    SheetTrigger,
    SheetContent,
} from "@/components/ui/sheet.jsx"
import { Button } from "@/components/ui/button.jsx"
import {Import} from "@/components/ui/Import.jsx"
import { Menu } from "lucide-react"
import {useMsal} from "@azure/msal-react";
import React from "react";
import {NavigationOption} from "@/components/ui/NavigationOption.jsx";

export const MainMenu = ({ state, dispatchState, reference}) => {
    const { t:translate } = useTranslation("common");
    const { instance: authenticator } = useMsal();
    const activeAccount = authenticator.getActiveAccount();

    const CONTENT = [
            {label:"LABEL_DASHBOARD",path:"/"},
            {label:"LABEL_BETS",path:"/bets"},
            {label:"LABEL_RULES",path:"/rules"},
            {label:"LABEL_ALERTS",path:"/alerts"},
    ];

    const onInitiateImport = () => dispatchState({
        type: ACTION_ON_INITIATE_IMPORT,
    });

    return (
            <div className="container mx-auto flex h-14 items-center px-4">
                <Import state={state} dispatchState={dispatchState} reference={reference} />
                {/* Desktop Navigation */}
                <div className="hidden md:flex">
                    <NavigationMenu >
                        <NavigationMenuList>
                            {
                                CONTENT.map((item, _) => (
                                    <NavigationOption
                                        key={item.label}
                                        state={state}
                                        dispatchState={dispatchState}
                                        reference={reference}
                                        resource={item.label}
                                        link={item.path}
                                        active={location.pathname === item.path}
                                    />
                                ))
                            }
                        </NavigationMenuList>
                    </NavigationMenu>
                </div>

                {/* Spacer */}
                <div className="flex-1" />

                <Button
                    variant="outline"
                    size="sm"
                    className="hidden md:inline-flex border-[#0FB7A6]"
                    disabled={!activeAccount}
                    onClick={onInitiateImport}
                >
                    {translate("LABEL_IMPORT_BETS")}
                </Button>

                {/* Mobile Hamburger Menu */}
                <Sheet>
                    <SheetTrigger className="ml-2 md:hidden">
                        <Menu className="h-6 w-6" />
                    </SheetTrigger>
                    <SheetContent side="left" className="p-4">
                        <div className="flex flex-col space-y-4">
                            {
                                CONTENT.map((item, _) => (
                                    <NavigationOption
                                        key={item.label}
                                        state={state}
                                        dispatchState={dispatchState}
                                        reference={reference}
                                        resource={item.label}
                                        link={item.path}
                                        mobile={true}
                                    />
                                ))
                            }
                            <Button className="w-full mt-4" disabled={!activeAccount}>
                                {translate("LABEL_IMPORT_BETS")}
                            </Button>
                        </div>
                    </SheetContent>
                </Sheet>
            </div>
    )
};
