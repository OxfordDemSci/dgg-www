BEGIN;
CREATE TABLE dgg(
		date            numeric (6) not null,
	    country         varchar(80) not null,
	    ISO3Code         char(3) not null,
	    ISO2Code         char(2),
	    Ground_Truth_Internet_GG  numeric  ,
	    Internet_Online_model_prediction numeric  ,
	    Internet_Online_Offline_model_prediction numeric  ,
		Internet_Offline_model_prediction numeric ,
	    Ground_Truth_Mobile_GG numeric ,
	    Mobile_Online_model_prediction numeric,
	    Mobile_Online_Offline_model_prediction numeric  ,
	    Mobile_Offline_model_prediction numeric
);

ALTER TABLE dgg ADD CONSTRAINT unique_date_country UNIQUE (date, country, ISO3Code);

COPY dgg(date, country, ISO3Code, ISO2Code,
    Ground_Truth_Internet_GG,Internet_Online_model_prediction,Internet_Online_Offline_model_prediction,Internet_Offline_model_prediction,
    Ground_Truth_Mobile_GG,Mobile_Online_model_prediction,Mobile_Online_Offline_model_prediction,Mobile_Offline_model_prediction)
FROM '/var/lib/postgresql/initial_data/mau_upper_monthly_model_2_2022-06.csv'
DELIMITER ','
CSV HEADER;

COPY dgg(date, country, ISO3Code, ISO2Code,
    Ground_Truth_Internet_GG,Internet_Online_model_prediction,Internet_Online_Offline_model_prediction,Internet_Offline_model_prediction,
    Ground_Truth_Mobile_GG,Mobile_Online_model_prediction,Mobile_Online_Offline_model_prediction,Mobile_Offline_model_prediction)
FROM '/var/lib/postgresql/initial_data/mau_upper_monthly_model_2_2022-07.csv'
DELIMITER ','
CSV HEADER;

COMMIT;
