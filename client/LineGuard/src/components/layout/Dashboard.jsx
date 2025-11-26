import {AuthenticatedTemplate, UnauthenticatedTemplate} from "@azure/msal-react";
import {Landing} from "@/components/layout/Landing.jsx";
import {ActiveBets} from "@/components/ui/ActiveBets.jsx";
import {HedgeOpportunities} from "@/components/ui/HedgeOpportunities.jsx";
import {UpcomingTriggers} from "@/components/ui/UpcomingTriggers.jsx";
import {RecentAlerts} from "@/components/ui/RecentAlerts.jsx";

export const Dashboard = ({ state, dispatchState, reference}) => {
    return (
        <>
            <AuthenticatedTemplate>
                <div className="container mx-auto px-4 py-10 space-y-10">

                    <section>
                        <h2 className="text-2xl font-semibold mb-4">Active Bets</h2>

                        <ActiveBets state={state} dispatchState={dispatchState} reference={reference} />
                    </section>
                    <section>
                        <h2 className="text-2xl font-semibold mb-4">Hedge Opportunities</h2>

                        <HedgeOpportunities state={state} dispatchState={dispatchState} reference={reference} />
                    </section>
                    <section>
                        <h2 className="text-2xl font-semibold mb-4">Upcoming Triggers</h2>

                        <UpcomingTriggers state={state} dispatchState={dispatchState} reference={reference} />
                    </section>
                    <section>
                        <h2 className="text-2xl font-semibold mb-4">Recent Alerts</h2>

                        <RecentAlerts state={state} dispatchState={dispatchState} reference={reference} />
                    </section>

                </div>
            </AuthenticatedTemplate>
            <UnauthenticatedTemplate>
                <Landing state={state} dispatchState={dispatchState} reference={reference}/>
            </UnauthenticatedTemplate>
        </>
    )
};