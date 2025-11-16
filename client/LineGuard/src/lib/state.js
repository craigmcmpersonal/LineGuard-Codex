import {log} from "@/lib/utilities.js";

const doReduceState = (state, action) => {
    switch (action.type) {
        default:
            return {
                ...state
            };
    }
};

export const initializeState = () => ({
});

export const reduceState = (state, action) => {
    const result = doReduceState(state, action);
    log(result);
    return result;
};