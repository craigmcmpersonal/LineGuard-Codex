import {NewRule} from "@/components/ui/NewRule.jsx";
import {ExistingRules} from "@/components/ui/ExistingRules.jsx";

export const Rules = ({ state, dispatchState, reference}) => {
    return (
        <div className="container mx-auto px-4 py-10 space-y-12">

            <div className="flex justify-between items-center">
                <h1 className="text-3xl font-bold">Your Hedging Rules</h1>
            </div>
            <section>
                <NewRule state={state} dispatchState={dispatchState} reference={reference} />
            </section>



            <section>
                <h2 className="text-2xl font-semibold mb-4">Your Rules</h2>

                <ExistingRules state={state} dispatchState={dispatchState} reference={reference} />
            </section>

        </div>
    )
};
