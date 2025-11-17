import "@/App.css";
import LogoText from "@/assets/logo-text.png";
import {initializeState, reduceState} from "@/lib/state.js";
import React from "react";
import {LABEL_LOGO_TEXT} from "@/lib/constants.js";
import { MainMenu} from "@/components/ui/MainMenu.jsx";
import {Header} from "@/components/layout/Header.jsx";
import {ProfileMenu} from "@/components/ui/ProfileMenu.jsx";
import {BrowserRouter,Route, Routes} from "react-router-dom";
import {Dashboard} from "@/components/ui/Dashboard.jsx";
import {Bets} from "@/components/ui/Bets.jsx";
import {Rules} from "@/components/ui/Rules.jsx";
import {Alerts} from "@/components/ui/Alerts.jsx";
import {Import} from "@/components/ui/Import.jsx";


export const App = () => {

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
                        <img src={LogoText} alt={LABEL_LOGO_TEXT} className="w-36" />
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
                <Route path="/" element={<Dashboard />} />
                <Route path="/bets" element={<Bets />} />
                <Route path="/rules" element={<Rules />} />
                <Route path="/alerts" element={<Alerts />} />
                <Route path="/import" element={<Import />} />
            </Routes>
        </main>
    </BrowserRouter>
  )
};
