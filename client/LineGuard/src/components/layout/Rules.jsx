import { useState } from "react"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Textarea } from "@/components/ui/textarea"
import { Pencil, Trash2, Sparkles } from "lucide-react"

export const Rules = ({ state, dispatchState, reference}) => {
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

        // In real app: call your rule interpreter API
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
        <div className="container mx-auto px-4 py-10 space-y-12">

            {/* ===== HEADER ===== */}
            <div className="flex justify-between items-center">
                <h1 className="text-3xl font-bold">Your Hedging Rules</h1>
            </div>



            {/* ===== ADD NEW RULE ===== */}
            <section>
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
            </section>



            {/* ===== EXISTING RULES LIST ===== */}
            <section>
                <h2 className="text-2xl font-semibold mb-4">Your Rules</h2>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {rules.map((rule) => (
                        <Card key={rule.id} className="flex flex-col">
                            <CardHeader>
                                <CardTitle className="flex justify-between items-center">
                  <span className="text-base font-medium truncate">
                    {rule.text}
                  </span>
                                    <Badge variant="outline">Active</Badge>
                                </CardTitle>
                            </CardHeader>

                            <CardContent className="flex-grow flex flex-col justify-between text-sm">

                                <div className="space-y-2 mb-4">
                                    {rule.parsed.map((p, index) => (
                                        <div
                                            key={index}
                                            className="text-muted-foreground flex items-start gap-2"
                                        >
                                            <span>•</span>
                                            <span>{p}</span>
                                        </div>
                                    ))}
                                </div>

                                <div className="flex justify-end gap-3 pt-4 border-t mt-4">
                                    <Button variant="outline" size="sm">
                                        <Pencil className="w-4 h-4 mr-2" />
                                        Edit
                                    </Button>

                                    <Button
                                        variant="destructive"
                                        size="sm"
                                        onClick={() =>
                                            setRules(rules.filter((r) => r.id !== rule.id))
                                        }
                                    >
                                        <Trash2 className="w-4 h-4 mr-2" />
                                        Delete
                                    </Button>
                                </div>

                            </CardContent>
                        </Card>
                    ))}
                </div>
            </section>

        </div>
    )
};
