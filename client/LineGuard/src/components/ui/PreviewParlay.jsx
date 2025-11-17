import { CheckCircle, Circle } from "lucide-react"
import {useTranslation} from "react-i18next";

export function PreviewParlay({state, dispatchState, reference, className}) {
    const { t:translate } = useTranslation("common");
    const CONTENT = [
        {key:"leg1", prefix:"Packers ML", suffixResource:"WON"},
        {key:"leg2", prefix:"Ravens -3.5", suffixResource:"WON"},
        {key:"leg3", prefix:"Under 43.5", suffixResource:"WON"},
        {key:"leg4", prefix:"Bengals ML", suffixResource:"WON"},
        {key:"leg5", prefix:"Jets +7", suffixResource:"WON"},
        {key:"leg6", prefix:"Seahawks +140", suffixResource:"LIVE"},
    ]
    return (
        <div className={`w-full bg-card border rounded-lg p-4 shadow ${className}`}>
            <div className="flex justify-between mb-2">
                <span className="font-medium">{translate("PREVIEW_PARLAY")}</span>
                <span className="text-sm text-muted-foreground">$25 → $310</span>
            </div>

            <div className="space-y-2 text-sm">
                {
                    CONTENT.map((item, index) => (
                        <div key={item.key} className="flex items-center gap-2">
                            <CheckCircle className="w-4 h-4 text-green-500" />
                            <span>{item.prefix} — {translate(item.suffixResource)}</span>
                        </div>
                    ))
                }
            </div>
        </div>
    )
}
