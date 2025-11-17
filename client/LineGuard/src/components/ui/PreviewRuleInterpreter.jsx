import {useTranslation} from "react-i18next";

export function PreviewRuleInterpreter({state, dispatchState, reference, className}) {
    const { t:translate } = useTranslation("common");
    const CONTENT_RESOURCES = [
        "PREVIEW_RULE_TRIGGER",
        "PREVIEW_RULE_ACTION",
        "PREVIEW_RULE_CONDITION",
        "PREVIEW_RULE_EXCEPTION",
    ];
    return (
        <div className={`w-full bg-card border rounded-lg p-4 shadow ${className}`}>
            <div className="text-sm text-muted-foreground">
                <div className="mb-2">
                  <span className="font-medium text-foreground">
                    {translate("PREVIEW_RULE")}
                  </span>
                </div>

                <ul className="list-disc pl-4 space-y-1 text-left">
                    {CONTENT_RESOURCES.map((item, _) => (
                        <li key={item}>
                            {translate(item)}
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    )
}
