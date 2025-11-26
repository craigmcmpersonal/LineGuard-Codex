import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card.jsx";
import {Badge} from "@/components/ui/badge.jsx";
import {CheckCircle, Circle} from "lucide-react";

export const ActiveBets = ({ state, dispatchState, reference}) => {
    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

            {/* Example Parlay */}
            <Card>
                <CardHeader>
                    <CardTitle className="flex justify-between">
                        <span>6-Leg NFL Parlay</span>
                        <Badge variant="outline">$25 → $310</Badge>
                    </CardTitle>
                </CardHeader>

                <CardContent className="space-y-2 text-sm">

                    <div className="flex items-center gap-2">
                        <CheckCircle className="w-4 h-4 text-green-500" />
                        <span>Packers ML — Won</span>
                    </div>

                    <div className="flex items-center gap-2">
                        <CheckCircle className="w-4 h-4 text-green-500" />
                        <span>Ravens -3.5 — Won</span>
                    </div>

                    <div className="flex items-center gap-2">
                        <CheckCircle className="w-4 h-4 text-green-500" />
                        <span>Under 43.5 — Won</span>
                    </div>

                    <div className="flex items-center gap-2">
                        <CheckCircle className="w-4 h-4 text-green-500" />
                        <span>Bengals ML — Won</span>
                    </div>

                    <div className="flex items-center gap-2">
                        <CheckCircle className="w-4 h-4 text-green-500" />
                        <span>Jets +7 — Won</span>
                    </div>

                    <div className="flex items-center gap-2">
                        <Circle className="w-4 h-4 text-primary" />
                        <span>Seahawks +140 — Live</span>
                    </div>

                </CardContent>
            </Card>

            {/* You’ll map real bets here later… */}
        </div>
)};