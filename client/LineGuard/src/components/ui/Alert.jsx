import {Card, CardContent} from "@/components/ui/card.jsx";
import {Badge} from "@/components/ui/badge.jsx";
import {Bell, CheckCircle, CircleDot, TrendingUp} from "lucide-react";

export const Alert = ({alert, state, dispatchState, reference}) => {
    const iconFor = (type) => {
        switch (type) {
            case "hedge":
                return <TrendingUp className="w-5 h-5 text-primary" />
            case "parlay":
                return <CheckCircle className="w-5 h-5 text-primary" />
            case "line":
                return <Bell className="w-5 h-5 text-primary" />
            default:
                return <CircleDot className="w-5 h-5 text-primary" />
        }
    }

    return (
        <Card
            key={alert.id}
            className={alert.unread ? "border-primary/40" : "opacity-80"}
        >
            <CardContent className="flex items-center justify-between py-4">

                {/* LEFT SIDE */}
                <div className="flex items-center gap-3">
                    {iconFor(alert.type)}

                    <div>
                        <div className="flex items-center gap-2">
                            <span className="font-medium">{alert.title}</span>
                            {alert.unread && (
                                <Badge className="bg-primary text-primary-foreground">
                                    New
                                </Badge>
                            )}
                        </div>
                        <p className="text-sm text-muted-foreground">
                            {alert.message}
                        </p>
                    </div>
                </div>

                {/* RIGHT SIDE */}
                <span className="text-sm text-muted-foreground whitespace-nowrap">
                {alert.timestamp}
              </span>

            </CardContent>
        </Card>
    )
};