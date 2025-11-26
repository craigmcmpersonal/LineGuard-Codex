import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card.jsx";

export const UpcomingTriggers = ({state, dispatchState, reference}) => {
    return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

            <Card>
                <CardHeader>
                    <CardTitle>Tonight 7:20 PM</CardTitle>
                </CardHeader>
                <CardContent className="text-sm text-muted-foreground">
                    Seahawks final leg becomes live.
                    Your “hedge underdogs” rule may activate.
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle>Line Movement Watch</CardTitle>
                </CardHeader>
                <CardContent className="text-sm text-muted-foreground">
                    Rams line moving from -180 → -195.
                    Alert will fire at -200.
                </CardContent>
            </Card>

        </div>
    )
};