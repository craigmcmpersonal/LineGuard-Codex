import { useState } from "react"
import { Button } from "@/components/ui/button"
import {
    Bell,
} from "lucide-react"
import {Alert} from "@/components/ui/Alert.jsx";
import {mockAlerts} from "@/lib/mock.js";


export const Alerts = ({state, dispatchState, reference}) => {

    const [alerts, setAlerts] = useState(mockAlerts())

    const markAllRead = () =>
        setAlerts(alerts.map((item) => ({ ...item, unread: false })))

    return (
        <div className="container mx-auto px-4 py-10 space-y-10">

            <div className="flex justify-between items-center">
                <h1 className="text-3xl font-bold">Alerts</h1>

                <Button
                    variant="outline"
                    onClick={markAllRead}
                    disabled={!alerts.some((item) => item.unread)}
                >
                    Mark all read
                </Button>
            </div>



            <section className="space-y-4">

                {alerts.map((item) => (
                    <Alert alert={item} state={state} dispatchState={dispatchState} reference={reference} />
                ))}

                {alerts.length === 0 && (
                    <div className="text-center text-muted-foreground py-20">
                        <Bell className="w-10 h-10 mx-auto mb-6 text-muted-foreground" />
                        <p>No alerts yet.</p>
                    </div>
                )}

            </section>

        </div>
    )
};
