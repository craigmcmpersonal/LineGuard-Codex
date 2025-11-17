import { TrendingUp } from "lucide-react"
import {useTranslation} from "react-i18next";

export function PreviewHedgeCalculator({state, dispatchState, reference, className}) {
    const { t:translate } = useTranslation("common");
    const CONTENT = [
        {resource:"LIVE_ODDS", color:"text-red-600", value:"+210"},
        {resource:"HEDGE_AMOUNT", color:"text-amber-600", value:"$57"},
        {resource:"GUARANTEED_PROFIT", color:"text-green-600", value:"$112"},
    ];
    return (
        <div className={`w-full bg-card border rounded-lg p-4 shadow ${className}`}>
            <div className="flex items-center gap-2 mb-3">
                <TrendingUp className="w-5 h-5 text-[#A7FF4A]" />
                <span className="font-medium">{translate("PREVIEW_HEDGE")}</span>
            </div>

            <div className="text-sm space-y-2">
                {
                    CONTENT.map((item, _) => (
                        <div key={item.resource} className="flex justify-between">
                            <span className="text-muted-foreground">{translate(item.resource)}</span>
                            <span className={`font-medium ${item.color}`}>{item.value}</span>
                        </div>
                    ))
                }
            </div>
        </div>
    )
}
