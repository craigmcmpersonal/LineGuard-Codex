CREATE TYPE public.outcome_enumeration AS ENUM
    ('Won', 'Lost', 'Voided', 'Half Won', 'Half Lost');

CREATE TYPE public.selection_status_enumeration AS ENUM
    ('Active', 'Suspended', 'Won', 'Lost', 'Voided');

CREATE TYPE public.alert_type_enumeration AS ENUM
    ('Hedge Opportunity', 'Rule Triggered', 'Odds Movement', 'Bet Status Change');

CREATE TYPE public.alert_type_enumeration AS ENUM
    ('Hedge Opportunity', 'Rule Triggered', 'Odds Movement', 'Bet Status Change');

CREATE TYPE public.bet_slip_source_enumeration AS ENUM
    ('Manual', 'Sync', 'Email', 'Image', 'Audio');

CREATE TYPE public.bet_slip_status_enumeration AS ENUM
    ('Pending', 'Placed', 'Won', 'Lost', 'Cashout Offered', 'Cashed Out', 'Voided', 'Partially Won');

CREATE TYPE public.bet_type_enumeration AS ENUM
    ('Single', 'Parlay', 'Teaser', 'Round Robin');

CREATE TYPE public.hedge_opportunity_status_enumeration AS ENUM
    ('Active', 'Executed', 'Expired');

CREATE TYPE public.market_status_enumeration AS ENUM
    ('Active', 'Suspended', 'Settled');

CREATE TYPE public.event_status_enumeration AS ENUM
    ('Scheduled', 'Live', 'Final', 'Cancelled', 'Postponed');

CREATE TABLE public."Bet_Leg" (
    key bigint CONSTRAINT "Bet_Leg_bet_leg_key_not_null" NOT NULL,
    bet_slip_key bigint NOT NULL,
    selection_key bigint NOT NULL,
    odds numeric(8,4) NOT NULL,
    status public.bet_leg_status_enumeration DEFAULT 'Pending'::public.bet_leg_status_enumeration NOT NULL,
    result public.outcome_enumeration,
    index integer NOT NULL,
    odds_live numeric(8,4),
    settled_time timestamp with time zone,
    public_key uuid DEFAULT gen_random_uuid() NOT NULL
);

CREATE TABLE public."Bet_Slip" (
    key bigint CONSTRAINT "Bet_Slip_bet_slip_key_not_null" NOT NULL,
    user_key uuid NOT NULL,
    total_odds numeric(10,4) NOT NULL,
    stake numeric(12,4) NOT NULL,
    status public.bet_slip_status_enumeration DEFAULT 'Pending'::public.bet_slip_status_enumeration NOT NULL,
    placed_time timestamp with time zone DEFAULT now() NOT NULL,
    settled_time timestamp with time zone,
    result public.outcome_enumeration,
    external_identifier text NOT NULL,
    book text NOT NULL,
    original bytea NOT NULL,
    model json,
    import_time timestamp with time zone DEFAULT now() NOT NULL,
    source public.bet_slip_source_enumeration NOT NULL,
    last_update_time timestamp with time zone DEFAULT now() NOT NULL,
    total_odds_live numeric(8,4),
    public_key uuid DEFAULT gen_random_uuid() NOT NULL
);

ALTER TABLE public."Bet_Slip" ALTER COLUMN key ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."Bet_Slip_bet_slip_key_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE public."Event" (
    key bigint CONSTRAINT "Event_event_key_not_null" NOT NULL,
    sport_key integer NOT NULL,
    name text NOT NULL,
    start_time timestamp with time zone NOT NULL,
    status public.event_status_enumeration DEFAULT 'Scheduled'::public.event_status_enumeration,
    public_key uuid DEFAULT gen_random_uuid() NOT NULL
);


ALTER TABLE public."Event" ALTER COLUMN key ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."Event_event_key_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE public."Hedge_Option" (
    key bigint NOT NULL,
    hedge_opportunity_key bigint NOT NULL,
    book text NOT NULL,
    odds numeric(8,4) NOT NULL,
    required_stake numeric(12,4) NOT NULL,
    guaranteed_profit numeric(12,4) NOT NULL,
    implied_probability numeric(5,4),
    option_rank integer DEFAULT 1,
    public_key uuid DEFAULT gen_random_uuid() NOT NULL,
    resource_location text,
    last_update_time timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public."Hedge_Option" ALTER COLUMN key ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."Hedge_Option_key_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE public."Hedge_Rule" (
    key bigint NOT NULL,
    user_hedge_profile_key bigint NOT NULL,
    rule_name text NOT NULL,
    original text NOT NULL,
    model json,
    priority integer DEFAULT 1 NOT NULL,
    active boolean DEFAULT true NOT NULL,
    creation_time timestamp with time zone DEFAULT now() NOT NULL
);

ALTER TABLE public."Hedge_Rule" ALTER COLUMN key ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."Hedge_Rule_key_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE public."Hege_Opportunity" (
    key bigint NOT NULL,
    bet_slip_key bigint NOT NULL,
    hedge_rule_key bigint NOT NULL,
    trigger_reason text,
    original_win_probability numeric(5,4),
    recommended_hedge_stake numeric(12,4),
    optimal_hedge_odds numeric(8,4),
    creation_time timestamp with time zone DEFAULT now() NOT NULL,
    expiration_time timestamp with time zone,
    status public.hedge_opportunity_status_enumeration
);


ALTER TABLE public."Hege_Opportunity" ALTER COLUMN key ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."Hege_Opportunity_key_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


CREATE TABLE public."Market" (
    key bigint CONSTRAINT "Market_market_key_not_null" NOT NULL,
    event_key bigint NOT NULL,
    market_type_key integer NOT NULL,
    name text NOT NULL,
    parameters json,
    status public.market_status_enumeration DEFAULT 'Active'::public.market_status_enumeration,
    public_key uuid DEFAULT gen_random_uuid()
);

COMMENT ON TABLE public."Market" IS 'A Market is an instance of a Market_Type for a specific Event. It links a sporting event to something within that event that one can bet on, such as the points spread for that specific game. ';

CREATE TABLE public."Market_Type" (
    key integer CONSTRAINT "Market_Type_market_type_key_not_null" NOT NULL,
    name text NOT NULL
);

COMMENT ON TABLE public."Market_Type" IS 'Types of things that one can bet on in relation to a sporting event. Examples include Moneyline, Point Spread, Player Prop, Next Play Outcome.';

ALTER TABLE public."Market_Type" ALTER COLUMN key ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."Market_Type_market_type_key_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


ALTER TABLE public."Market" ALTER COLUMN key ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."Market_market_key_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


CREATE TABLE public."Selection" (
    key bigint CONSTRAINT "Selection_selection_key_not_null" NOT NULL,
    event_key bigint NOT NULL,
    market_key bigint NOT NULL,
    name text NOT NULL,
    odds numeric(8,4) NOT NULL,
    status public.selection_status_enumeration DEFAULT 'Active'::public.selection_status_enumeration,
    outcome public.outcome_enumeration,
    public_key uuid DEFAULT gen_random_uuid()
);


COMMENT ON TABLE public."Selection" IS 'A specific, bettable outcome within a Market';


ALTER TABLE public."Selection" ALTER COLUMN key ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."Selection_selection_key_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


CREATE TABLE public."Sport" (
    key integer CONSTRAINT "Sport_sport_key_not_null" NOT NULL,
    name text NOT NULL,
    active boolean DEFAULT true NOT NULL
);


ALTER TABLE public."Sport" ALTER COLUMN key ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."Sport_sport_key_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE public."User_Alert" (
    key bigint NOT NULL,
    user_key text NOT NULL,
    hedge_opportunity_key bigint,
    title text NOT NULL,
    message text NOT NULL,
    read boolean DEFAULT false NOT NULL,
    resource_location text,
    creation_time timestamp with time zone DEFAULT now() NOT NULL,
    sent_time timestamp with time zone,
    public_key uuid DEFAULT gen_random_uuid()
);


ALTER TABLE public."User_Alert" ALTER COLUMN key ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."User_Alert_key_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE public."User_Hedge_Profile" (
    key bigint NOT NULL,
    user_key text NOT NULL,
    content text NOT NULL,
    active boolean DEFAULT true NOT NULL,
    creation_time timestamp with time zone DEFAULT now() NOT NULL
);

ALTER TABLE public."User_Hedge_Profile" ALTER COLUMN key ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."User_Hedge_Profile_key_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

ALTER TABLE ONLY public."Bet_Leg"
    ADD CONSTRAINT "Bet_Leg_pkey" PRIMARY KEY (key);

ALTER TABLE ONLY public."Bet_Slip"
    ADD CONSTRAINT "Bet_Slip_pkey" PRIMARY KEY (key);

ALTER TABLE ONLY public."Event"
    ADD CONSTRAINT "Event_pkey" PRIMARY KEY (key);

ALTER TABLE ONLY public."Hedge_Option"
    ADD CONSTRAINT "Hedge_Option_pkey" PRIMARY KEY (key);

ALTER TABLE ONLY public."Hedge_Rule"
    ADD CONSTRAINT "Hedge_Rule_pkey" PRIMARY KEY (key);

ALTER TABLE ONLY public."Hege_Opportunity"
    ADD CONSTRAINT "Hege_Opportunity_pkey" PRIMARY KEY (key);

ALTER TABLE ONLY public."Market_Type"
    ADD CONSTRAINT "Market_Type_pkey" PRIMARY KEY (key);

ALTER TABLE ONLY public."Market"
    ADD CONSTRAINT "Market_pkey" PRIMARY KEY (key);

ALTER TABLE ONLY public."Selection"
    ADD CONSTRAINT "Selection_pkey" PRIMARY KEY (key);

ALTER TABLE ONLY public."Sport"
    ADD CONSTRAINT "Sport_pkey" PRIMARY KEY (key);

ALTER TABLE ONLY public."User_Alert"
    ADD CONSTRAINT "User_Alert_pkey" PRIMARY KEY (key);

ALTER TABLE ONLY public."User_Hedge_Profile"
    ADD CONSTRAINT "User_Hedge_Profile_pkey" PRIMARY KEY (key);

ALTER TABLE ONLY public."Market_Type"
    ADD CONSTRAINT market_type_name_unique UNIQUE (name);

ALTER TABLE ONLY public."Sport"
    ADD CONSTRAINT sport_name_unique UNIQUE (name);

ALTER TABLE ONLY public."Bet_Leg"
    ADD CONSTRAINT bet_leg_selection FOREIGN KEY (selection_key) REFERENCES public."Selection"(key);

ALTER TABLE ONLY public."Bet_Leg"
    ADD CONSTRAINT bet_leg_x_bet_slip FOREIGN KEY (bet_slip_key) REFERENCES public."Bet_Slip"(key);

ALTER TABLE ONLY public."Event"
    ADD CONSTRAINT event_x_sport FOREIGN KEY (sport_key) REFERENCES public."Sport"(key) NOT VALID;

ALTER TABLE ONLY public."Hege_Opportunity"
    ADD CONSTRAINT hedge_opportunity_x_bet_slip FOREIGN KEY (bet_slip_key) REFERENCES public."Bet_Slip"(key) NOT VALID;

ALTER TABLE ONLY public."Hege_Opportunity"
    ADD CONSTRAINT hedge_opportunity_x_hedge_rule FOREIGN KEY (hedge_rule_key) REFERENCES public."Hedge_Rule"(key) NOT VALID;

ALTER TABLE ONLY public."Hedge_Option"
    ADD CONSTRAINT hedge_option_x_hedge_opportunity FOREIGN KEY (hedge_opportunity_key) REFERENCES public."Hege_Opportunity"(key);

ALTER TABLE ONLY public."Hedge_Rule"
    ADD CONSTRAINT hege_rule_x_user_hedge_profile FOREIGN KEY (user_hedge_profile_key) REFERENCES public."User_Hedge_Profile"(key);

ALTER TABLE ONLY public."Market"
    ADD CONSTRAINT market_x_event FOREIGN KEY (event_key) REFERENCES public."Event"(key);

ALTER TABLE ONLY public."Market"
    ADD CONSTRAINT market_x_market_type FOREIGN KEY (market_type_key) REFERENCES public."Market_Type"(key) NOT VALID;

ALTER TABLE ONLY public."Selection"
    ADD CONSTRAINT selection_x_event FOREIGN KEY (event_key) REFERENCES public."Event"(key);

ALTER TABLE ONLY public."Selection"
    ADD CONSTRAINT selection_x_market FOREIGN KEY (market_key) REFERENCES public."Market"(key);

ALTER TABLE ONLY public."User_Alert"
    ADD CONSTRAINT user_alert_x_hedge_opportunity FOREIGN KEY (hedge_opportunity_key) REFERENCES public."Hege_Opportunity"(key);




