import {EMPTY_STRING} from "@//lib/constants.js";

export const Header = ({ state, dispatchState, reference, left, center, right, className = EMPTY_STRING }) => {
    return (
        <header className={`bg-background shadow-sm border-b border-border ${className}`}>
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="grid grid-cols-3 items-center h-16">
                    <div className="flex items-center">
                        {left}
                    </div>
                    <div className="flex justify-center">
                        {center}
                    </div>
                    <div className="flex items-center justify-end space-x-2">
                        {right}
                    </div>
                </div>
            </div>
        </header>
    );
};


