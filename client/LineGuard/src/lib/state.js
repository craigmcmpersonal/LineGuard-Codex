import {log} from "@/lib/utilities.js";

export const ACTION_ON_CANCEL_IMPORT = "ON_CANCEL_IMPORT";
export const ACTION_ON_INITIATE_IMPORT = "ON_INITIATE_IMPORT";

const doReduceState = (state, action) => {
    switch (action.type) {
        case ACTION_ON_CANCEL_IMPORT:
            return {
                ...state,
                importInitiated: false,
            };
        case ACTION_ON_INITIATE_IMPORT:
            return {
                ...state,
                importInitiated: true,
            };
        default:
            return {
                ...state
            };
    }
};

export const initializeState = () => ({
    importInitiated: true
});

export const reduceState = (state, action) => {
    const result = doReduceState(state, action);
    log(result);
    return result;
};