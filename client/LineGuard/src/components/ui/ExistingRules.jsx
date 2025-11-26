import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card.jsx";
import {Badge} from "@/components/ui/badge.jsx";
import {Button} from "@/components/ui/button.jsx";
import {Pencil, Trash2} from "lucide-react";

export const ExistingRules = ({state, dispatchState, reference}) => {
    return (
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
    )
};