import "@/App.css";
import LogoText from "@/assets/logo-text.png";
import {initializeState, reduceState} from "@/lib/state.js";
import React from "react";
import {LABEL_LOGO_TEXT} from "@/lib/constants.js";
import {MainMenu} from "@/components/ui/MainMenu.jsx";
import {Header} from "@/components/layout/Header.jsx";
import {ProfileMenu} from "@/components/ui/ProfileMenu.jsx";


export const App = () => {

    const onLoad = () => {
    };

    const reference = React.useRef({cancelled: false});
    const [state, dispatchState] = React.useReducer(reduceState, initializeState());
    React.useEffect(onLoad, []);

  return (
    <>
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
    </>
  )
};
