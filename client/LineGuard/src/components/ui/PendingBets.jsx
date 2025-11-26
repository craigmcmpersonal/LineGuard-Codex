import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card.jsx";
import {Badge} from "@/components/ui/badge.jsx";

export const PendingBets = ({state, dispatchState, reference}) => {
    return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

            <Card>
                <CardHeader>
                    <CardTitle className="flex justify-between">
                        <span>Chiefs -3.0</span>
                        <Badge>Pending</Badge>
                    </CardTitle>
                </CardHeader>

                <CardContent className="text-sm text-muted-foreground">
                    Game starts tonight at 5:20 PM.
                </CardContent>
            </Card>

        </div>
    )
};