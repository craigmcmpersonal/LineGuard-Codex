export function isString(value) {
    return typeof value === "string" || value instanceof String;
}

export const log = (value) => {
    if (value) {
        try {
            const text = isString(value) ? value : JSON.stringify(value)
            console.info(text);
        }
        catch (exception) {
            console.warn(`${value} ${exception}`);
        }
    }
};