import {AuthenticatedTemplate, UnauthenticatedTemplate} from "@azure/msal-react";
import {Landing} from "@/components/layout/Landing.jsx";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { CheckCircle, Circle, TrendingUp, Bell } from "lucide-react"

export const Dashboard = ({ state, dispatchState, reference}) => {
    return (
        <>
            <AuthenticatedTemplate>
                <div className="container mx-auto px-4 py-10 space-y-10">

                    {/* ====== ACTIVE BETS ====== */}
                    <section>
                        <h2 className="text-2xl font-semibold mb-4">Active Bets</h2>

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

                            {/* Additional bet cards would go here */}
                        </div>
                    </section>



                    {/* ====== HEDGE OPPORTUNITIES ====== */}
                    <section>
                        <h2 className="text-2xl font-semibold mb-4">Hedge Opportunities</h2>

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
                    </section>



                    {/* ====== UPCOMING TRIGGERS ====== */}
                    <section>
                        <h2 className="text-2xl font-semibold mb-4">Upcoming Triggers</h2>

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
                    </section>



                    {/* ====== ALERT FEED ====== */}
                    <section>
                        <h2 className="text-2xl font-semibold mb-4">Recent Alerts</h2>

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
                    </section>

                </div>
            </AuthenticatedTemplate>
            <UnauthenticatedTemplate>
                <Landing state={state} dispatchState={dispatchState} reference={reference}/>
            </UnauthenticatedTemplate>
        </>

    )
};