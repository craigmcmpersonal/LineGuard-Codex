import {ActiveBets} from "@/components/ui/ActiveBets.jsx"
import { Button } from "@/components/ui/button"
import { Upload } from "lucide-react"
import {PendingBets} from "@/components/ui/PendingBets.jsx";
import {SettledBets} from "@/components/ui/SettledBets.jsx";

export const Bets = ({ state, dispatchState, reference, onImport}) => {
    return (
        <div className="container mx-auto px-4 py-10 space-y-10">

            <div className="flex justify-between items-center">
                <h1 className="text-3xl font-bold">Your Bets</h1>
                <Button onClick={onImport}>
                    <Upload className="w-4 h-4 mr-2" />
                    Import Bets
                </Button>
            </div>
            <section>
                <h2 className="text-2xl font-semibold mb-4">Active</h2>

                <ActiveBets state={state} dispatchState={dispatchState} reference={reference}/>
            </section>
            <section>
                <h2 className="text-2xl font-semibold mb-4">Pending</h2>

                <PendingBets state={state} dispatchState={dispatchState} reference={reference}/>
            </section>
            <section>
                <h2 className="text-2xl font-semibold mb-4">Settled</h2>

                <SettledBets state={state} dispatchState={dispatchState} reference={reference}/>
            </section>

        </div>
    )
};