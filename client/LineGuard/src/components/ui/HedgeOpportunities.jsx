import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card.jsx";
import {Badge} from "@/components/ui/badge.jsx";
import {Button} from "@/components/ui/button.jsx";

export const HedgeOpportunities = ({state, dispatchState, reference}) => {
    return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

            <Card>
                <CardHeader>
                    <CardTitle className="flex justify-between">
                        <span>Seahawks +140 (Final Leg)</span>
                        <Badge className="bg-green-100 text-green-800">Rule Triggered</Badge>
                    </CardTitle>
                </CardHeader>

                <CardContent className="space-y-3 text-sm">

                    <div className="flex justify-between">
                        <span className="text-muted-foreground">Live Odds</span>
                        <span className="font-medium">+210</span>
                    </div>

                    <div className="flex justify-between">
                        <span className="text-muted-foreground">Hedge Amount</span>
                        <span className="font-medium">$57</span>
                    </div>

                    <div className="flex justify-between">
                        <span className="text-muted-foreground">Guaranteed Profit</span>
                        <span className="font-medium text-green-600">$112</span>
                    </div>

                    <Button className="w-full">View Hedge Options</Button>
                </CardContent>
            </Card>

        </div>
    )
};