psql -U $POSTGRES_USER -d $POSTGRES_DB -c \
"
CREATE ROLE dgg_reader LOGIN PASSWORD '${POSTGRES_RPASS}';
CREATE ROLE dgg_writer LOGIN PASSWORD '${POSTGRES_WPASS}';

CREATE TABLE country_info(
    iso2 CHAR(2) PRIMARY KEY,
    iso3 CHAR(3) NOT NULL,
    name VARCHAR(80) NOT NULL,
    UNIQUE (iso2, iso3, name)
);

GRANT SELECT ON country_info TO dgg_reader;
GRANT SELECT, INSERT ON country_info TO dgg_writer;

CREATE TABLE national(
    id SERIAL PRIMARY KEY,
    created TIMESTAMPTZ(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0),
    iso2 CHAR(2) NOT NULL,
    date numeric (6) NOT NULL,
    Ground_Truth_Internet_GG NUMERIC,
    Internet_Online_model_prediction NUMERIC,
    Internet_Online_Offline_model_prediction NUMERIC,
    Internet_Offline_model_prediction NUMERIC,
    Ground_Truth_Mobile_GG NUMERIC,
    Mobile_Online_model_prediction NUMERIC,
    Mobile_Online_Offline_model_prediction NUMERIC,
    Mobile_Offline_model_prediction NUMERIC,
    UNIQUE (date, iso2),
    FOREIGN KEY(iso2) REFERENCES country_info(iso2) ON DELETE SET NULL
);

CREATE INDEX idx_national_date ON national(date);

GRANT SELECT ON national TO dgg_reader;
GRANT SELECT, INSERT ON national TO dgg_writer;
GRANT USAGE,SELECT ON SEQUENCE national_id_seq TO dgg_writer;
"
psql -U $POSTGRES_USER -d $POSTGRES_DB -c \
"
COPY country_info(name, iso2, iso3)
FROM '/var/lib/postgresql/initial_data/country_info.csv'
DELIMITER ','
CSV HEADER;

COPY national(iso2, date, 
    ground_truth_internet_gg,internet_online_model_prediction,internet_online_offline_model_prediction,internet_offline_model_prediction,
    ground_truth_mobile_gg,mobile_online_model_prediction,mobile_online_offline_model_prediction,mobile_offline_model_prediction)
FROM '/var/lib/postgresql/initial_data/national.csv'
DELIMITER ','
CSV HEADER;
"