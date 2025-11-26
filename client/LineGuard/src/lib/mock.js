export const mockAlerts = () => [
    {
        id: 1,
        type: "hedge",
        title: "Hedge opportunity found",
        message: "Seahawks final leg qualifies for your hedge rule.",
        timestamp: "2 min ago",
        unread: true,
    },
    {
        id: 2,
        type: "parlay",
        title: "Parlay now one leg away",
        message: "Your 6-leg NFL parlay is 5/6 completed.",
        timestamp: "1 hour ago",
        unread: false,
    },
    {
        id: 3,
        type: "line",
        title: "Line movement approaching threshold",
        message: "Rams line moved from -180 → -195.",
        timestamp: "3 hours ago",
        unread: false,
    },
];