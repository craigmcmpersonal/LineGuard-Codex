import {useTranslation} from "react-i18next";
import {useMsal} from "@azure/msal-react";
import {NavigationMenuItem, NavigationMenuLink} from "@/components/ui/navigation-menu.jsx";

export const NavigationOption = ({ state, dispatchState, reference, resource, link, mobile=false}) => {
    const { t:translate } = useTranslation("common");
    const { instance: authenticator } = useMsal();
    const activeAccount = authenticator.getActiveAccount();

    return (
        mobile ?
            <a
                href="/link"
                className={cn(
                    "text-lg font-medium px-2 py-1",
                    !activeAccount && "pointer-events-none opacity-50 cursor-not-allowed"
                )}
            >
                resource
            </a>
            : <NavigationMenuItem>
                {activeAccount
                    ? (
                        <NavigationMenuLink href={link}>
                            {translate(resource)}
                        </NavigationMenuLink>
                    )
                    : (
                        <span className="text-muted-foreground cursor-not-allowed opacity-50 px-4 py-2">
                          {translate(resource)}
                        </span>
                    )}
            </NavigationMenuItem>
    )
}