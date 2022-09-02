BEGIN;
CREATE TABLE dgg(
		date            numeric (6) not null,
	    country         varchar(80) not null,
	    ISO3Code         char(3) not null,
	    ISO2Code         char(2) not null,
	    Ground_Truth_Internet_GG  numeric  ,
	    Internet_Online_model_prediction numeric  ,
	    Internet_Online_Offline_model_prediction numeric  ,
		Internet_Offline_model_prediction numeric ,
	    Ground_Truth_Mobile_GG numeric ,
	    Mobile_Online_model_prediction numeric,
	    Mobile_Online_Offline_model_prediction numeric  ,
	    Mobile_Offline_model_prediction numeric
);
ALTER TABLE dgg ADD CONSTRAINT unique_date_country UNIQUE (date, country, ISO3Code, ISO2Code);
COMMIT;
