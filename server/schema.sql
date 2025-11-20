CREATE TYPE public.bet_leg_status_enumeration AS ENUM
    ('Pending', 'Won', 'Lost', 'Voided');

CREATE TYPE public.outcome_enumeration AS ENUM
    ('Won', 'Lost', 'Voided', 'Half Won', 'Half Lost');

CREATE TYPE public.selection_status_enumeration AS ENUM
    ('Active', 'Suspended', 'Won', 'Lost', 'Voided');

CREATE TYPE public.bet_leg_status_enumeration AS ENUM
    ('Pending', 'Won', 'Lost', 'Voided');

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

CREATE TYPE public.sport_type_enumeration AS ENUM
    ('Game', 'Race', 'Fight', 'Tournament');

CREATE TYPE public.sport_type_enumeration AS ENUM
('Game', 'Race', 'Fight', 'Tournament');

CREATE TABLE IF NOT EXISTS public."Entrant"
(
    key bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    name text COLLATE pg_catalog."default" NOT NULL,
    "number" text COLLATE pg_catalog."default",
    event_key bigint NOT NULL,
    CONSTRAINT "Entrant_pkey" PRIMARY KEY (key),
    CONSTRAINT entrant_x_event FOREIGN KEY (event_key)
    REFERENCES public."Event" (key) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS public."Race_Result"
(
    key bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    event_key bigint NOT NULL,
    "position" integer NOT NULL,
    win_payout numeric(8,2),
    place_payout numeric(8,2),
    entrant_key bigint NOT NULL,
    CONSTRAINT "Race_Result_pkey" PRIMARY KEY (key),
    CONSTRAINT race_result_unique_event_entrant_position UNIQUE (event_key, entrant_key, "position"),
    CONSTRAINT race_result_x_entrant FOREIGN KEY (entrant_key)
        REFERENCES public."Entrant" (key) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT race_result_x_event FOREIGN KEY (event_key)
        REFERENCES public."Event" (key) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS public."Sport"
(
    key integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name text COLLATE pg_catalog."default" NOT NULL,
    active boolean NOT NULL DEFAULT true,
    sport_type_key sport_type_enumeration NOT NULL DEFAULT 'Game'::sport_type_enumeration,
    CONSTRAINT "Sport_pkey" PRIMARY KEY (key),
    CONSTRAINT sport_name_unique UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS public."Bet_Slip"
(
    key bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    user_key uuid NOT NULL,
    total_odds numeric(10,4) NOT NULL,
    stake numeric(12,4) NOT NULL,
    status bet_slip_status_enumeration NOT NULL DEFAULT 'Pending'::bet_slip_status_enumeration,
    placed_time timestamp with time zone NOT NULL DEFAULT now(),
    settled_time timestamp with time zone,
    result outcome_enumeration,
    external_identifier text COLLATE pg_catalog."default" NOT NULL,
    book text COLLATE pg_catalog."default" NOT NULL,
    original bytea NOT NULL,
    model jsonb,
    import_time timestamp with time zone NOT NULL DEFAULT now(),
    source bet_slip_source_enumeration NOT NULL,
    last_update_time timestamp with time zone NOT NULL DEFAULT now(),
    total_odds_live numeric(8,4),
    public_key uuid NOT NULL DEFAULT gen_random_uuid(),
    will_pay numeric(12,4),
    CONSTRAINT "Bet_Slip_pkey" PRIMARY KEY (key),
    CONSTRAINT bet_slip_unique_source UNIQUE (user_key, book, external_identifier)
);

CREATE TABLE IF NOT EXISTS public."Selection"
(
    key bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    event_key bigint NOT NULL,
    market_key bigint NOT NULL,
    odds numeric(8,4) NOT NULL,
    status selection_status_enumeration NOT NULL DEFAULT 'Active'::selection_status_enumeration,
    outcome outcome_enumeration,
    public_key uuid NOT NULL DEFAULT gen_random_uuid(),
    "position" integer NOT NULL DEFAULT 1,
    entrant_key bigint,
    CONSTRAINT "Selection_pkey" PRIMARY KEY (key),
    CONSTRAINT selection_unique_public_key UNIQUE (public_key),
    CONSTRAINT select_x_entrant FOREIGN KEY (entrant_key)
    REFERENCES public."Entrant" (key) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID,
    CONSTRAINT selection_x_event FOREIGN KEY (event_key)
    REFERENCES public."Event" (key) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION,
    CONSTRAINT selection_x_market FOREIGN KEY (market_key)
    REFERENCES public."Market" (key) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
);

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


CREATE TABLE public."Bet_Leg_Odds_History" (
    key bigint NOT NULL,
    bet_leg_key bigint NOT NULL,
    book text NOT NULL,
    odds numeric(8,4) NOT NULL,
    captured_time timestamp with time zone DEFAULT now() NOT NULL
);

ALTER TABLE public."Bet_Leg_Odds_History" ALTER COLUMN key ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."Bet_Leg_Odds_History_key_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
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
    model jsonb,
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

CREATE TABLE public."Hedge_Opportunity" (
    key bigint CONSTRAINT "Hege_Opportunity_key_not_null" NOT NULL,
    bet_slip_key bigint CONSTRAINT "Hege_Opportunity_bet_slip_key_not_null" NOT NULL,
    hedge_rule_key bigint CONSTRAINT "Hege_Opportunity_hedge_rule_key_not_null" NOT NULL,
    trigger_reason text,
    original_win_probability numeric(5,4),
    recommended_hedge_stake numeric(12,4),
    optimal_hedge_odds numeric(8,4),
    creation_time timestamp with time zone DEFAULT now() CONSTRAINT "Hege_Opportunity_creation_time_not_null" NOT NULL,
    expiration_time timestamp with time zone,
    status public.hedge_opportunity_status_enumeration DEFAULT 'Active'::public.hedge_opportunity_status_enumeration
);


CREATE TABLE public."Hedge_Opportunity_Leg" (
    key bigint CONSTRAINT "Hege_Opportunity_Leg_key_not_null" NOT NULL,
    hedge_opportunity_key bigint CONSTRAINT "Hege_Opportunity_Leg_hedge_opportunity_key_not_null" NOT NULL,
    bet_leg_key bigint CONSTRAINT "Hege_Opportunity_Leg_bet_leg_key_not_null" NOT NULL
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
    model jsonb,
    priority integer DEFAULT 1 NOT NULL,
    active boolean DEFAULT true NOT NULL,
    creation_time timestamp with time zone DEFAULT now() NOT NULL,
    version integer DEFAULT 1 NOT NULL,
    valid_from timestamp with time zone DEFAULT now() NOT NULL,
    valid_to timestamp with time zone
);


CREATE TABLE public."Hedge_Rule_Filter" (
    key bigint NOT NULL,
    hedge_rule_key bigint NOT NULL,
    sport_key integer,
    market_type_key integer,
    minimum_odds numeric(8,4),
    maximum_odds numeric(8,4)
);


ALTER TABLE public."Hedge_Rule_Filter" ALTER COLUMN key ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."Hedge_Rule_Filter_key_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


ALTER TABLE public."Hedge_Rule" ALTER COLUMN key ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."Hedge_Rule_key_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


CREATE TABLE public."Hedge_Rule_x_Bet_Slip" (
    hedge_rule_key bigint CONSTRAINT "Hedge_Rule_Bet_Slip_hedge_rule_key_not_null" NOT NULL,
    bet_slip_key bigint CONSTRAINT "Hedge_Rule_Bet_Slip_bet_slip_key_not_null" NOT NULL
);


ALTER TABLE public."Hedge_Opportunity" ALTER COLUMN key ADD GENERATED ALWAYS AS IDENTITY (
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
    parameters jsonb,
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

CREATE TABLE public."Rule_Evaluation_Log" (
    key bigint NOT NULL,
    hedge_rule_key bigint NOT NULL,
    bet_slip_key bigint NOT NULL,
    evaluation_time timestamp with time zone DEFAULT now() NOT NULL,
    inputs jsonb NOT NULL,
    output jsonb NOT NULL,
    hedge_opportunity_key bigint
);

ALTER TABLE public."Rule_Evaluation_Log" ALTER COLUMN key ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."Rule_Evaluation_Log_key_seq"
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
    hedge_opportunity_key bigint,
    title text NOT NULL,
    message text NOT NULL,
    read boolean DEFAULT false NOT NULL,
    resource_location text,
    creation_time timestamp with time zone DEFAULT now() NOT NULL,
    sent_time timestamp with time zone,
    public_key uuid DEFAULT gen_random_uuid(),
    user_key uuid,
    type public.alert_type_enumeration
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
    content text NOT NULL,
    creation_time timestamp with time zone DEFAULT now() NOT NULL,
    user_key uuid,
    version integer DEFAULT 1 NOT NULL,
    valid_from timestamp with time zone DEFAULT now() NOT NULL,
    valid_to timestamp with time zone
);

ALTER TABLE public."User_Hedge_Profile" ALTER COLUMN key ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."User_Hedge_Profile_key_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

ALTER TABLE ONLY public."Bet_Leg_Odds_History"
    ADD CONSTRAINT "Bet_Leg_Odds_History_pkey" PRIMARY KEY (key);

ALTER TABLE ONLY public."Bet_Leg"
    ADD CONSTRAINT "Bet_Leg_pkey" PRIMARY KEY (key);

ALTER TABLE ONLY public."Bet_Slip"
    ADD CONSTRAINT "Bet_Slip_pkey" PRIMARY KEY (key);

ALTER TABLE ONLY public."Event"
    ADD CONSTRAINT "Event_pkey" PRIMARY KEY (key);

ALTER TABLE ONLY public."Hedge_Opportunity_Leg"
    ADD CONSTRAINT "Hedge_Opportunity_Leg_pkey" PRIMARY KEY (key);

ALTER TABLE ONLY public."Hedge_Opportunity"
    ADD CONSTRAINT "Hedge_Opportunity_pkey" PRIMARY KEY (key);

ALTER TABLE ONLY public."Hedge_Option"
    ADD CONSTRAINT "Hedge_Option_pkey" PRIMARY KEY (key);

ALTER TABLE ONLY public."Hedge_Rule_x_Bet_Slip"
    ADD CONSTRAINT "Hedge_Rule_Bet_Slip_pkey" PRIMARY KEY (hedge_rule_key, bet_slip_key);

ALTER TABLE ONLY public."Hedge_Rule_Filter"
    ADD CONSTRAINT "Hedge_Rule_Filter_pkey" PRIMARY KEY (key);

ALTER TABLE ONLY public."Hedge_Rule"
    ADD CONSTRAINT "Hedge_Rule_pkey" PRIMARY KEY (key);

ALTER TABLE ONLY public."Market_Type"
    ADD CONSTRAINT "Market_Type_pkey" PRIMARY KEY (key);

ALTER TABLE ONLY public."Market"
    ADD CONSTRAINT "Market_pkey" PRIMARY KEY (key);

ALTER TABLE ONLY public."Rule_Evaluation_Log"
    ADD CONSTRAINT "Rule_Evaluation_Log_pkey" PRIMARY KEY (key);

ALTER TABLE ONLY public."Selection"
    ADD CONSTRAINT "Selection_pkey" PRIMARY KEY (key);

ALTER TABLE ONLY public."Sport"
    ADD CONSTRAINT "Sport_pkey" PRIMARY KEY (key);

ALTER TABLE ONLY public."User_Alert"
    ADD CONSTRAINT "User_Alert_pkey" PRIMARY KEY (key);

ALTER TABLE ONLY public."User_Hedge_Profile"
    ADD CONSTRAINT "User_Hedge_Profile_pkey" PRIMARY KEY (key);

ALTER TABLE ONLY public."Bet_Slip"
    ADD CONSTRAINT bet_slip_unique_source UNIQUE (user_key, book, external_identifier);

ALTER TABLE ONLY public."Hedge_Rule"
    ADD CONSTRAINT hedge_rule_unique_version UNIQUE (user_hedge_profile_key, rule_name, version);

ALTER TABLE ONLY public."Market_Type"
    ADD CONSTRAINT market_type_name_unique UNIQUE (name);

ALTER TABLE ONLY public."Sport"
    ADD CONSTRAINT sport_name_unique UNIQUE (name);

ALTER TABLE ONLY public."Hedge_Opportunity_Leg"
    ADD CONSTRAINT "Hedge_Opportunity_Leg_x_Bet_Leg" FOREIGN KEY (bet_leg_key) REFERENCES public."Bet_Leg"(key) NOT VALID;

ALTER TABLE ONLY public."Hedge_Opportunity_Leg"
    ADD CONSTRAINT "Hedge_Opportunity_Leg_x_Hedge_Opportunity" FOREIGN KEY (hedge_opportunity_key) REFERENCES public."Hedge_Opportunity"(key) NOT VALID;

ALTER TABLE ONLY public."Rule_Evaluation_Log"
    ADD CONSTRAINT "Rule_Evaluation_Log_x_Bet_Slip_Key" FOREIGN KEY (bet_slip_key) REFERENCES public."Bet_Slip"(key);

ALTER TABLE ONLY public."Rule_Evaluation_Log"
    ADD CONSTRAINT "Rule_Evaluation_Log_x_Hedge_Opportunity" FOREIGN KEY (hedge_opportunity_key) REFERENCES public."Hedge_Opportunity"(key);

ALTER TABLE ONLY public."Rule_Evaluation_Log"
    ADD CONSTRAINT "Rule_Evaluation_Log_x_Hedge_Rule" FOREIGN KEY (hedge_rule_key) REFERENCES public."Hedge_Rule"(key);

ALTER TABLE ONLY public."Bet_Leg_Odds_History"
    ADD CONSTRAINT bet_leg_odds_history_x_bet_leg FOREIGN KEY (bet_leg_key) REFERENCES public."Bet_Leg"(key) NOT VALID;

ALTER TABLE ONLY public."Bet_Leg"
    ADD CONSTRAINT bet_leg_selection FOREIGN KEY (selection_key) REFERENCES public."Selection"(key);

ALTER TABLE ONLY public."Bet_Leg"
    ADD CONSTRAINT bet_leg_x_bet_slip FOREIGN KEY (bet_slip_key) REFERENCES public."Bet_Slip"(key);

ALTER TABLE ONLY public."Event"
    ADD CONSTRAINT event_x_sport FOREIGN KEY (sport_key) REFERENCES public."Sport"(key) NOT VALID;

ALTER TABLE ONLY public."Hedge_Opportunity"
    ADD CONSTRAINT hedge_opportunity_x_bet_slip FOREIGN KEY (bet_slip_key) REFERENCES public."Bet_Slip"(key) NOT VALID;

ALTER TABLE ONLY public."Hedge_Opportunity"
    ADD CONSTRAINT hedge_opportunity_x_hedge_rule FOREIGN KEY (hedge_rule_key) REFERENCES public."Hedge_Rule"(key) NOT VALID;

ALTER TABLE ONLY public."Hedge_Option"
    ADD CONSTRAINT hedge_option_x_hedge_opportunity FOREIGN KEY (hedge_opportunity_key) REFERENCES public."Hedge_Opportunity"(key);

ALTER TABLE ONLY public."Hedge_Rule_Filter"
    ADD CONSTRAINT hedge_rule_filter_x_hedge_rule FOREIGN KEY (hedge_rule_key) REFERENCES public."Hedge_Rule"(key);

ALTER TABLE ONLY public."Hedge_Rule_Filter"
    ADD CONSTRAINT hedge_rule_filter_x_market_type FOREIGN KEY (market_type_key) REFERENCES public."Market_Type"(key);

ALTER TABLE ONLY public."Hedge_Rule_Filter"
    ADD CONSTRAINT hedge_rule_filter_x_sport FOREIGN KEY (sport_key) REFERENCES public."Sport"(key);

ALTER TABLE ONLY public."Hedge_Rule_x_Bet_Slip"
    ADD CONSTRAINT hedge_rule_x_bet_slip_x_bet_slip FOREIGN KEY (bet_slip_key) REFERENCES public."Bet_Slip"(key);

ALTER TABLE ONLY public."Hedge_Rule_x_Bet_Slip"
    ADD CONSTRAINT hedge_rule_x_bet_slip_x_hedge_rule FOREIGN KEY (hedge_rule_key) REFERENCES public."Hedge_Rule"(key);

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
    ADD CONSTRAINT user_alert_x_hedge_opportunity FOREIGN KEY (hedge_opportunity_key) REFERENCES public."Hedge_Opportunity"(key);


