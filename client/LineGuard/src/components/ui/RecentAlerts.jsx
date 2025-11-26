import {Card, CardContent} from "@/components/ui/card.jsx";
import {Bell} from "lucide-react";

export const RecentAlerts  = ({state, dispatchState, reference}) => {
    return (
        <div className="grid grid-cols-1 gap-4">

            <Card>
                <CardContent className="flex items-center justify-between py-4">
                    <div className="flex items-center gap-3">
                        <Bell className="w-5 h-5 text-primary" />
                        <span>Hedge opportunity found for Seahawks final leg.</span>
                    </div>
                    <span className="text-sm text-muted-foreground">2 min ago</span>
                </CardContent>
            </Card>

            <Card>
                <CardContent className="flex items-center justify-between py-4">
                    <div className="flex items-center gap-3">
                        <Bell className="w-5 h-5 text-primary" />
                        <span>Your parlay is one leg away.</span>
                    </div>
                    <span className="text-sm text-muted-foreground">1 hour ago</span>
                </CardContent>
            </Card>

        </div>
    )
};