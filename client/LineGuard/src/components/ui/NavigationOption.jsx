import {useTranslation} from "react-i18next";
import {useMsal} from "@azure/msal-react";
import {NavigationMenuItem, NavigationMenuLink} from "@/components/ui/navigation-menu.jsx";
import {cn} from "@/lib/utils";

export const NavigationOption = ({
    state,
    dispatchState,
    reference,
    resource,
    link,
    isActive = false,
    mobile=false
}) => {
    const { t:translate } = useTranslation("common");
    const { instance: authenticator } = useMsal();
    const activeAccount = authenticator.getActiveAccount();

    return (
        mobile ?
            <a
                href={link}
                className={cn(
                    "text-lg font-medium px-2 py-1",
                    isActive ? "bg-accent text-accent-foreground rounded-md" : "text-foreground",
                    !activeAccount && "pointer-events-none opacity-50 cursor-not-allowed"
                )}
            >
                {translate(resource)}
            </a>
            : <NavigationMenuItem>
                {activeAccount
                    ? (
                        <NavigationMenuLink
                            href={link}
                            data-active={isActive}
                        >
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
