import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { CheckCircle, Circle, XCircle, Upload } from "lucide-react"

export const Bets = ({ state, dispatchState, reference, onImport}) => {
    return (
        <div className="container mx-auto px-4 py-10 space-y-10">

            {/* ====== Header Row ====== */}
            <div className="flex justify-between items-center">
                <h1 className="text-3xl font-bold">Your Bets</h1>
                <Button onClick={onImport}>
                    <Upload className="w-4 h-4 mr-2" />
                    Import Bets
                </Button>
            </div>



            {/* ====== ACTIVE BETS ====== */}
            <section>
                <h2 className="text-2xl font-semibold mb-4">Active</h2>

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
            </section>





            {/* ====== PENDING BETS ====== */}
            <section>
                <h2 className="text-2xl font-semibold mb-4">Pending</h2>

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
            </section>




            {/* ====== SETTLED BETS ====== */}
            <section>
                <h2 className="text-2xl font-semibold mb-4">Settled</h2>

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
            </section>

        </div>
    )
};