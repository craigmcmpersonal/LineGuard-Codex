import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card.jsx";
import {Sparkles} from "lucide-react";
import {Textarea} from "@/components/ui/textarea.jsx";
import {Button} from "@/components/ui/button.jsx";

export const NewRule = ({state, dispatchState, reference}) => {
    const [ruleText, setRuleText] = useState("")
    const [rules, setRules] = useState([
        {
            id: 1,
            text: "If the last leg is an underdog, hedge fully.",
            parsed: [
                "Trigger: final leg is an underdog",
                "Action: full hedge",
                "Condition: odds movement > 20%"
            ]
        },
        {
            id: 2,
            text: "Hedge parlays when only one leg remains.",
            parsed: [
                "Trigger: parlay reaches final leg",
                "Action: recommend full hedge"
            ]
        }
    ])

    const handleAddRule = () => {
        if (!ruleText.trim()) return

        const newRule = {
            id: Date.now(),
            text: ruleText,
            parsed: [
                "Trigger: parsed trigger example",
                "Action: parsed action example",
                "Condition: parsed condition example"
            ]
        }

        setRules([...rules, newRule])
        setRuleText("")
    }

    return (
        <Card className="max-w-3xl">
            <CardHeader>
                <CardTitle className="flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-primary" />
                    Add a New Rule
                </CardTitle>
            </CardHeader>

            <CardContent className="space-y-6">

                <div>
                    <p className="text-sm text-muted-foreground mb-2">
                        Describe your hedging rule in plain English:
                    </p>

                    <Textarea
                        placeholder='Example: "If the final leg is an underdog, hedge fully."'
                        value={ruleText}
                        onChange={(e) => setRuleText(e.target.value)}
                        className="min-h-[100px]"
                    />
                </div>

                <div className="flex justify-end">
                    <Button onClick={handleAddRule}>Save Rule</Button>
                </div>
            </CardContent>
        </Card>
    )
};