import { useTranslation } from "react-i18next";
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Shield, LineChart, Bell, Sparkles, Upload } from "lucide-react"
import {AuthenticationButton} from "@/components/ui/AuthenticationButton.jsx";
import React from "react";
import {PreviewParlay} from "@/components/ui/PreviewParlay.jsx";
import {PreviewRuleInterpreter} from "@/components/ui/PreviewRuleInterpreter.jsx";
import {PreviewHedgeCalculator} from "@/components/ui/PreviewHedgeCalculator.jsx";

export const Landing = ({ state, dispatchState, reference}) => {
    const { t:translate } = useTranslation("common");
    const EXPLANATIONS = [
        {
            key:"EXPLANATION_IMPORT",
            heading:"LANDING_IMPORT_HEADING",
            subHeading:"LANDING_IMPORT_SUB_HEADING",
            icon:<Upload className="w-8 h-8 mb-2 text-primary" />
        },
        {
            key:"EXPLANATION_RULES",
            heading:"LANDING_RULES_HEADING",
            subHeading:"LANDING_RULES_SUB_HEADING",
            icon:<Sparkles className="w-8 h-8 mb-2 text-primary" />
        },
        {
            key:"EXPLANATION_MONITOR",
            heading:"LANDING_MONITOR_HEADING",
            subHeading:"LANDING_MONITOR_SUB_HEADING",
            icon:<LineChart className="w-8 h-8 mb-2 text-primary" />
        },
        {
            key:"EXPLANATION_ALERTS",
            heading:"LANDING_ALERTS_HEADING",
            subHeading:"LANDING_ALERTS_SUB_HEADING",
            icon:<Bell className="w-8 h-8 mb-2 text-primary" />
        },
    ];
    const FEATURES = [
        {
            key:"FEATURES_PARLAY_TRACKING",
            heading:"LANDING_PARLAY_TRACKING_HEADING",
            subHeading:"LANDING_PARLAY_TRACKING_SUB_HEADING",
            preview:<PreviewParlay
                state={state}
                dispatchState={dispatchState}
                reference={reference}
                className="mb-4"
            />
        },
        {
            key:"EXPLANATION_RULE_INTERPRETER",
            heading:"LANDING_RULE_INTERPRETER_HEADING",
            subHeading:"LANDING_RULE_INTERPRETER_SUB_HEADING",
            preview:<PreviewRuleInterpreter
                state={state}
                dispatchState={dispatchState}
                reference={reference}
                className="mb-4"
            />
        },
        {
            key:"EXPLANATION_CALCULATOR",
            heading:"LANDING_CALCULATOR_HEADING",
            subHeading:"LANDING_CALCULATOR_SUB_HEADING",
            preview:<PreviewHedgeCalculator
                state={state}
                dispatchState={dispatchState}
                reference={reference}
                className="mb-4"  />
        },
    ];
    const TRUST_ELEMENTS = [
        {
            key:"TRUST_BOOKS",
            resource:"LANDING_TRUST_ITEM_BOOKS",
        },
        {
            key:"TRUST_PAYMENT",
            resource:"LANDING_TRUST_ITEM_PAYMENT",
        },
        {
            key:"TRUST_DATA",
            resource:"LANDING_TRUST_ITEM_DATA",
        },
    ];
    const FOOTER_ELEMENTS = [
        {
            key:"FOOTER_PRIVACY",
            resource:"LABEL_PRIVACY",
            link:"/privacy",
        },
        {
            key:"FOOTER_TERMS",
            resource:"LABEL_TERMS",
            link:"/terms",
        },
        {
            key:"FOOTER_SUPPORT",
            resource:"LABEL_SUPPORT",
            link:"/support",
        },
    ];
    return (
        <div className="w-full flex flex-col items-center">
            {/* HERO SECTION */}
            <section className="w-full max-w-5xl text-center py-20 px-6">
                <h1 className="text-4xl md:text-5xl font-bold mb-6">
                    {translate("HERO_TEXT")}
                </h1>

                <p className="text-lg md:text-xl text-muted-foreground mb-10 max-w-3xl mx-auto">
                    {translate("HERO_SUB_HEADING")}
                </p>

                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                    <AuthenticationButton
                        state={state}
                        dispatchState={dispatchState}
                        reference={reference}
                        variant="default"
                        size="lg"
                        label={translate("LABEL_LANDING_START")}
                    />
                    <Button size="lg" variant="outline" onClick={() => {
                        document.getElementById("explanation")?.scrollIntoView({ behavior: "smooth" })
                    }}>
                        {translate("How It Works")}
                    </Button>
                </div>
            </section>

            {/* HOW IT WORKS */}
            <section id="explanation" className="w-full max-w-6xl px-6 py-20">
                <h2 className="text-3xl font-semibold text-center mb-12">How It Works</h2>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                    {EXPLANATIONS.map((item, _) => (
                        <Card key={item.key}>
                            <CardHeader>
                                {item.icon}
                                <CardTitle>{translate(item.heading)}</CardTitle>
                            </CardHeader>
                            <CardContent className="text-muted-foreground">
                                {translate(item.subHeading)}
                            </CardContent>
                        </Card>
                    ))}
                </div>
            </section>

            {/* FEATURE WALKTHROUGH */}
            <section className="w-full max-w-6xl px-6 py-20">
                <h2 className="text-3xl font-semibold text-center mb-12">Inside the App</h2>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
                    {FEATURES.map((item, _) => (
                        <Card key={item.key} className="h-full flex flex-col">
                            <CardHeader>
                                <CardTitle>{translate(item.heading)}</CardTitle>
                            </CardHeader>
                            <CardContent className="text-muted-foreground flex flex-col h-full">
                                <div className="flex-grow">
                                    {item.preview}
                                </div>
                                <p className="pt-4">{translate(item.subHeading)}</p>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            </section>

            {/* CALL TO ACTION STRIPE */}
            <section className="w-full py-16 bg-muted text-center px-6">
                <h3 className="text-2xl font-semibold mb-6">
                    {translate("LANDING_CALL_TO_ACTION")}
                </h3>
                <AuthenticationButton
                    state={state}
                    dispatchState={dispatchState}
                    reference={reference}
                    variant="default"
                    size="lg"
                    label={translate("LABEL_LANDING_CALL_TO_ACTION")}
                />
            </section>

            {/* TRUST & SAFETY */}
            <section className="w-full max-w-4xl px-6 py-20 text-center">
                <Shield className="w-10 h-10 mx-auto mb-4 text-primary" />

                <h4 className="text-xl font-semibold mb-4">{translate("LANDING_TRUST_HEADING")}</h4>

                <p className="text-muted-foreground max-w-2xl mx-auto">
                    {translate("LANDING_TRUST_SUB_HEADING")}
                </p>

                <ul className="mt-6 space-y-2 text-muted-foreground mx-auto w-fit text-left">
                    {
                        TRUST_ELEMENTS.map((item, _) => (
                            <li key={item.key}>• {translate(item.resource)}</li>
                        ))
                    }
                </ul>
            </section>

            {/* FOOTER */}
            <footer className="w-full py-12 text-center text-muted-foreground text-sm">
                <div className="space-x-6">
                    {
                        FOOTER_ELEMENTS.map((item, _) => (
                            <a
                                key={item.key}
                                href={item.link}
                                className="hover:underline">
                                    {translate(item.resource)}
                            </a>
                        ))
                    }
                </div>
            </footer>
        </div>
    );
};