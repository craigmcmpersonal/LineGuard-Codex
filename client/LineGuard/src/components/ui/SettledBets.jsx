import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card.jsx";
import {Badge} from "@/components/ui/badge.jsx";
import {CheckCircle, XCircle} from "lucide-react";

export const SettledBets = ({state, dispatchState, reference}) => {
    return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

            <Card>
                <CardHeader>
                    <CardTitle className="flex justify-between">
                        <span>49ers ML</span>
                        <Badge className="bg-green-100 text-green-800">Won</Badge>
                    </CardTitle>
                </CardHeader>

                <CardContent className="flex items-center gap-2 text-sm">
                    <CheckCircle className="w-4 h-4 text-green-600" />
                    <span>You won $85</span>
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle className="flex justify-between">
                        <span>Lakers +4.5</span>
                        <Badge className="bg-red-100 text-red-800">Lost</Badge>
                    </CardTitle>
                </CardHeader>

                <CardContent className="flex items-center gap-2 text-sm">
                    <XCircle className="w-4 h-4 text-red-600" />
                    <span>Lost $25</span>
                </CardContent>
            </Card>

        </div>
    )
};