import "@/App.css";
import LogoText from "@/assets/logo-text.png";
import {initializeState, reduceState} from "@/lib/state.js";
import { useTranslation } from "react-i18next";
import React from "react";
import { MainMenu} from "@/components/layout/MainMenu.jsx";
import {Header} from "@/components/layout/Header.jsx";
import {ProfileMenu} from "@/components/layout/ProfileMenu.jsx";
import {BrowserRouter,Route, Routes} from "react-router-dom";
import {Dashboard} from "@/components/layout/Dashboard.jsx";
import {Bets} from "@/components/layout/Bets.jsx";
import {Rules} from "@/components/layout/Rules.jsx";
import {Alerts} from "@/components/layout/Alerts.jsx";
import {Import} from "@/components/ui/Import.jsx";
import {Privacy} from "@/components/layout/Privacy.jsx";
import {Terms} from "@/components/layout/Terms.jsx";
import {Support} from "@/components/layout/Support.jsx";


export const App = () => {
    const { t: translate} = useTranslation("common");

    const onLoad = () => {
    };

    const reference = React.useRef({cancelled: false});
    const [state, dispatchState] = React.useReducer(reduceState, initializeState());
    React.useEffect(onLoad, []);

  return (
    <BrowserRouter>
        <Header state={state}
                dispatchState={dispatchState}
                reference={reference}
                left={
                    <div className="flex items-center space-x-2">
                        <img src={LogoText} alt={translate("LOGO_TEXT")} className="w-36" />
                    </div>
                }
                center={
                    <MainMenu state={state} dispatchState={dispatchState} reference={reference} />
                }
                right={
                    <ProfileMenu state={state} dispatchState={dispatchState} reference={reference}/>
                }
        />
        <main className="p-6">
            <Routes>
                <Route
                    path="/"
                    element={<Dashboard state={state} dispatchState={dispatchState} reference={reference}/>}
                />
                <Route
                    path="/bets"
                    element={<Bets state={state} dispatchState={dispatchState} reference={reference}/>}
                />
                <Route
                    path="/rules"
                    element={<Rules state={state} dispatchState={dispatchState} reference={reference}/>}
                />
                <Route
                    path="/alerts"
                    element={<Alerts state={state} dispatchState={dispatchState} reference={reference}/>}
                />
                <Route
                    path="/import"
                    element={<Import state={state} dispatchState={dispatchState} reference={reference}/>}
                />
                <Route
                    path="/privacy"
                    element={<Privacy state={state} dispatchState={dispatchState} reference={reference}/>}
                />
                <Route
                    path="/terms"
                    element={<Terms state={state} dispatchState={dispatchState} reference={reference}/>}
                />
                <Route
                    path="/support"
                    element={<Support state={state} dispatchState={dispatchState} reference={reference}/>}
                />
            </Routes>
        </main>
    </BrowserRouter>
  )
};
