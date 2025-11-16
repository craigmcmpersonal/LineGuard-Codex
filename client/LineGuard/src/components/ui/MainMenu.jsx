import {
    NavigationMenu,
    NavigationMenuList,
    NavigationMenuItem,
    NavigationMenuLink,
} from "@/components/ui/navigation-menu"

import {
    Sheet,
    SheetTrigger,
    SheetContent,
} from "@/components/ui/sheet"

import { Button } from "@/components/ui/button"
import { Menu } from "lucide-react"

export const MainMenu = () => {
    return (
            <div className="container mx-auto flex h-14 items-center px-4">
                {/* Desktop Navigation */}
                <div className="hidden md:flex">
                    <NavigationMenu>
                        <NavigationMenuList>

                            <NavigationMenuItem>
                                <NavigationMenuLink href="/dashboard">
                                    Dashboard
                                </NavigationMenuLink>
                            </NavigationMenuItem>

                            <NavigationMenuItem>
                                <NavigationMenuLink href="/bets">
                                    Bets
                                </NavigationMenuLink>
                            </NavigationMenuItem>

                            <NavigationMenuItem>
                                <NavigationMenuLink href="/rules">
                                    Rules
                                </NavigationMenuLink>
                            </NavigationMenuItem>

                            <NavigationMenuItem>
                                <NavigationMenuLink href="/alerts">
                                    Alerts
                                </NavigationMenuLink>
                            </NavigationMenuItem>

                        </NavigationMenuList>
                    </NavigationMenu>
                </div>

                {/* Spacer */}
                <div className="flex-1" />

                {/* Import Bets button */}
                <Button variant="outline" size="sm" className="hidden md:inline-flex border-[#0FB7A6]">
                    Import Bets
                </Button>

                {/* Mobile Hamburger Menu */}
                <Sheet>
                    <SheetTrigger className="ml-2 md:hidden">
                        <Menu className="h-6 w-6" />
                    </SheetTrigger>
                    <SheetContent side="left" className="p-4">
                        <div className="flex flex-col space-y-4">
                            <a href="/dashboard" className="text-lg font-medium">
                                Dashboard
                            </a>
                            <a href="/bets" className="text-lg font-medium">
                                Bets
                            </a>
                            <a href="/rules" className="text-lg font-medium">
                                Rules
                            </a>
                            <a href="/alerts" className="text-lg font-medium">
                                Alerts
                            </a>
                            <Button className="w-full mt-4">
                                Import Bets
                            </Button>
                        </div>
                    </SheetContent>
                </Sheet>
            </div>
    )
}
