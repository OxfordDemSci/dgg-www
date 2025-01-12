import sqlalchemy
from sqlalchemy import text, distinct
from flask import Response
from typing import Any, Optional
from sqlalchemy import text
import math

from app import db
from .datatypes import CountriesEnum3
from .models import (
    SubNationalIndicators,
    NationalIndicators,
    SubNationalGroundTruth,
    NationalGroundTruth,
    SubNationalNames,
    DGGIndicatorDescription,
    User
)

from sqlalchemy.orm import sessionmaker


def get_user(username: str) -> Optional[User]:
    user = db.session.query(User).filter_by(username=username).first()
    return user


def dq_get_init_data() -> dict[str, dict[str, list[dict[str, str]]]]:
    result = {}
    national_countries_query = db.session.query(NationalIndicators.gid_0, NationalIndicators.country).distinct()
    national_dates_query = db.session.query(NationalIndicators.date).distinct()
    national_outcomes_query = db.session.query(NationalIndicators.outcome).distinct()
    indicator_descriptions_query = db.session.query(DGGIndicatorDescription).all()

    national_ground_truth_query = (
        db.session.query(
            NationalGroundTruth.gid_0,
            NationalIndicators.country
        )
        .join(NationalIndicators, NationalIndicators.gid_0 == NationalGroundTruth.gid_0)
        .distinct()
    )
    
    subnational_ground_truth_query = (
        db.session.query(
            SubNationalGroundTruth.gid_0,
            SubNationalGroundTruth.gid_1,
            SubNationalNames.country,
            SubNationalNames.name_1
        )
        .join(SubNationalNames, SubNationalNames.gid_1 == SubNationalGroundTruth.gid_1)
        .distinct()
    )

    national_countries = [{"iso3code": x.gid_0, "country": x.country} for x in national_countries_query.all()]
    national_dates = [x[0] for x in national_dates_query.all()]
    national_outcomes = [x.outcome for x in national_outcomes_query.all()]
    national_ground_truth_countries = [{"iso3code": x.gid_0, "country": x.country} for x in national_ground_truth_query.all()]
    subnational_ground_truth_regions = [{"admin_id": x.gid_1, "iso3code": x.gid_0, "country": x.country, "region_name": x.name_1} for x in subnational_ground_truth_query.all()]

    descriptions = {}
    for desc in indicator_descriptions_query:
        descriptions[desc.indicator_type] = {
            "mobile_women": {
                "name": "Mobile Women",
                "description": desc.mobile_women_description
            },
            "mobile_men": {
                "name": "Mobile Men",
                "description": desc.mobile_men_description
            },
            "mobile_fm_ratio": {
                "name": "Mobile Gender Gap",
                "description": desc.mobile_gender_gap_description
            },
            "internet_women": {
                "name": "Internet Women",
                "description": desc.internet_women_description
            },
            "internet_men": {
                "name": "Internet Men",
                "description": desc.internet_men_description
            },
            "internet_fm_ratio": {
                "name": "Internet Gender Gap",
                "description": desc.internet_gender_gap_description
            },
            "data_frequency": desc.data_frequency,
            "geographical_coverage": desc.geographical_coverage
        }

    result["national"] = {
        "countries": national_countries,
        "dates": sorted(national_dates),
        "models": national_outcomes
    }

    subnational_regions_query = db.session.query(
        SubNationalNames.gid_1,
        SubNationalNames.gid_0,
        SubNationalNames.country,
        SubNationalNames.name_1
    ).order_by(SubNationalNames.gid_0, SubNationalNames.gid_1).distinct()
    subnational_dates_query = db.session.query(SubNationalIndicators.date).distinct()
    subnational_outcomes_query = db.session.query(SubNationalIndicators.outcome).distinct()
    subnational_regions = [
        {
            "admin_id": x.gid_1,
            "iso3code": x.gid_0,
            "country": x.country,
            "region_name": x.name_1
        } for x in subnational_regions_query.all()
    ]
    subnational_dates = [x[0] for x in subnational_dates_query.all()]
    subnational_outcomes = [x.outcome for x in subnational_outcomes_query.all()]
    result["subnational"] = {
        "regions": subnational_regions,
        "dates": sorted(subnational_dates),
        "models": subnational_outcomes
    }
    result["national_ground_truth"] = national_ground_truth_countries
    result["subnational_ground_truth"] = subnational_ground_truth_regions

    result["descriptions"] = descriptions

    return result


def dq_query_outcomes_by_date(date: str) -> dict[str, list[dict[str, Any]]]:
    national_query = db.session.query(NationalIndicators.outcome).filter(NationalIndicators.date == date).distinct()
    subnational_query = db.session.query(SubNationalIndicators.outcome).filter(SubNationalIndicators.date == date).distinct()

    national_outcomes = [row[0] for row in national_query.all()]
    subnational_outcomes = [row[0] for row in subnational_query.all()]

    outcomes_to_check = [
        "internet_men",
        "internet_women",
        "mobile_women",
        "internet_fm_ratio",
        "mobile_fm_ratio",
        "mobile_men"
    ]

    result = {}
    result["national"] = {outcome: (outcome in national_outcomes) for outcome in outcomes_to_check}
    result["subnational"] = {outcome: (outcome in subnational_outcomes) for outcome in outcomes_to_check}
    return result


def dq_query_specific_country(country: str, indicators: list[str] | None = None):
    query = db.session.query(NationalIndicators).filter(NationalIndicators.gid_0 == country).order_by(NationalIndicators.date)
    
    if indicators is not None and len(indicators) > 0:
        query = query.filter(NationalIndicators.outcome.in_(indicators))
    
    results: list[NationalIndicators] = query.all()
    
    response: dict[str, dict[str, dict[str, float]]] = {}
    for result in results:
        gid_0_value = str(result.gid_0)
        outcome = str(result.outcome)
        predicted = round(float(result.predicted), 3)
        predicted_error = round(float(result.predicted_error), 3)
        date_key = result.date
        if result.gid_0 not in response:
            response[gid_0_value] = {}
        if date_key not in response[gid_0_value]:
            response[gid_0_value][date_key] = {}
        response[gid_0_value][date_key][outcome] = {"predicted": predicted, "predicted_error": predicted_error}
    return response


def dq_query_specific_region(region: str, indicators: list[str] | None = None):
    query = db.session.query(SubNationalIndicators).filter(SubNationalIndicators.gid_1 == region).order_by(SubNationalIndicators.date)
    
    if indicators is not None and len(indicators) > 0:
        query = query.filter(SubNationalIndicators.outcome.in_(indicators))
    
    results: list[SubNationalIndicators] = query.all()
    
    response: dict[str, dict[str, dict[str, float]]] = {}
    for result in results:
        gid_1_value = str(result.gid_1)
        outcome = str(result.outcome)
        predicted = round((result.predicted), 3)
        predicted_error = round((result.predicted_error), 3)
        date_key = result.date
        if result.gid_1 not in response:
            response[gid_1_value] = {}
        if date_key not in response[gid_1_value]:
            response[gid_1_value][date_key] = {}
        response[gid_1_value][date_key][outcome] = {"predicted": predicted, "predicted_error": predicted_error}
    return response


def dq_query_national_data(date: str, indicators: list[str] | None = None):
    query = db.session.query(NationalIndicators).filter(NationalIndicators.date == date)

    if indicators is not None and len(indicators) > 0:
        query = query.filter(NationalIndicators.outcome.in_(indicators))

    results: list[NationalIndicators] = query.all()

    response: dict[str, dict[str, float]] = {}
    for result in results:
        gid_0_value = str(result.gid_0)
        outcome = str(result.outcome)
        predicted = round(float(result.predicted), 3)
        predicted_error = round(float(result.predicted_error), 3)
        if result.gid_0 not in response:
            response[gid_0_value] = {}
        response[gid_0_value][outcome] = {"predicted": predicted, "predicted_error": predicted_error}
    return response


def dq_query_subnational_data(
        date: str,
        country: str | None = None,
        indicators: list[str] | None = None):
    query = db.session.query(SubNationalIndicators).filter(SubNationalIndicators.date == date)

    if country is not None:
        query = query.filter(SubNationalIndicators.gid_0 == country)

    if indicators is not None and len(indicators) > 0:
        query = query.filter(SubNationalIndicators.outcome.in_(indicators))

    results: list[SubNationalIndicators] = query.all()

    response: dict[str, dict[str, dict[str, float]]] = {}
    for result in results:
        gid_0_value = str(result.gid_0)
        gid_1_value = str(result.gid_1)
        outcome = str(result.outcome)
        predicted = round(float(result.predicted), 3)
        predicted_error = round(float(result.predicted_error), 3)

        if gid_0_value not in response:
            response[gid_0_value] = {}
        if gid_1_value not in response[gid_0_value]:
            response[gid_0_value][gid_1_value] = {}

        response[gid_0_value][gid_1_value][outcome] = {"predicted": predicted, "predicted_error": predicted_error}

    return response


def dq_download_national_data_with_dates(start_date: str, end_date: str, country: str | None = None):
    query = db.session.query(NationalIndicators).filter(NationalIndicators.date.between(start_date, end_date)).order_by(NationalIndicators.date)

    if country is not None:
        query = query.filter(NationalIndicators.gid_0 == country)

    results: list[NationalIndicators] = query.all()

    response: dict[str, dict[str, dict[str, float]]] = {}
    for result in results:
        gid_0_value = str(result.gid_0)
        outcome = str(result.outcome)
        predicted = round(float(result.predicted), 3) if not math.isnan(result.predicted) else None
        predicted_error = round(float(result.predicted_error), 3) if not math.isnan(result.predicted_error) else None
        date_key = result.date
        if result.gid_0 not in response:
            response[gid_0_value] = {}
        if date_key not in response[gid_0_value]:
            response[gid_0_value][date_key] = {}
        response[gid_0_value][date_key][outcome] = {"predicted": predicted, "predicted_error": predicted_error}
    return response


def dq_download_subnational_data_with_dates(start_date: str, end_date: str, region: str | None = None):
    query = db.session.query(SubNationalIndicators).filter(SubNationalIndicators.date.between(start_date, end_date)).order_by(SubNationalIndicators.date)

    if region is not None:
        query = query.filter(SubNationalIndicators.gid_1 == region)

    results: list[SubNationalIndicators] = query.all()

    response: dict[str, dict[str, dict[str, dict[str, float]]]] = {}
    for result in results:
        gid_0_value = str(result.gid_0)
        gid_1_value = str(result.gid_1)
        outcome = str(result.outcome)
        predicted = round(float(result.predicted), 3) if not math.isnan(result.predicted) else None
        predicted_error = round(float(result.predicted_error), 3) if not math.isnan(result.predicted_error) else None
        date_key = result.date
        
        if gid_0_value not in response:
            response[gid_0_value] = {}
        if gid_1_value not in response[gid_0_value]:
            response[gid_0_value][gid_1_value] = {}
        if date_key not in response[gid_0_value][gid_1_value]:
            response[gid_0_value][gid_1_value][date_key] = {}
        
        response[gid_0_value][gid_1_value][date_key][outcome] = {"predicted": predicted, "predicted_error": predicted_error}

    return response


def dq_get_ground_truth_subnational(indicators: list[str] | None = None):
    query = db.session.query(SubNationalGroundTruth).order_by(SubNationalGroundTruth.gid_0, SubNationalGroundTruth.gid_1)

    if indicators is not None and len(indicators) > 0:
        query = query.filter(SubNationalGroundTruth.outcome.in_(indicators))

    results: list[SubNationalGroundTruth] = query.all()

    response: dict[str, dict[str, dict[str, Any]]] = {}
    for result in results:
        gid_0_value = str(result.gid_0)
        gid_1_value = str(result.gid_1)
        survey_year = str(result.survey_year)
        outcome = str(result.outcome)
        observed = round(float(result.observed), 3)
        source = str(result.source)
        
        if gid_0_value not in response:
            response[gid_0_value] = {}
        if gid_1_value not in response[gid_0_value]:
            response[gid_0_value][gid_1_value] = {}
        
        response[gid_0_value][gid_1_value][outcome] = observed
        response[gid_0_value][gid_1_value]["survey_year"] = survey_year
        response[gid_0_value][gid_1_value]["source"] = source

    return response


def dq_get_ground_truth_national(indicators: list[str] | None = None):
    query = db.session.query(NationalGroundTruth).order_by(NationalGroundTruth.gid_0)

    if indicators is not None and len(indicators) > 0:
        query = query.filter(NationalGroundTruth.outcome.in_(indicators))

    results: list[NationalGroundTruth] = query.all()

    response: dict[str, dict[str, Any]] = {}
    for result in results:
        gid_0_value = str(result.gid_0)
        survey_year = str(result.survey_year)
        outcome = str(result.outcome)
        observed = round(float(result.observed), 3)
        source = str(result.source)
        if result.gid_0 not in response:
            response[gid_0_value] = {}
        response[gid_0_value][outcome] = observed
        response[gid_0_value]["survey_year"] = survey_year
        response[gid_0_value]["source"] = source

    return response


def dq_download_national_data_csv(start_date: str, end_date: str, indicators: list[str] | None = None):
    start_date = start_date + "-01"
    end_date = end_date + "-01"
    query = text(
        """
        SELECT * from national_indicators
        WHERE date BETWEEN :start_date AND :end_date;
        """
    )
    results = db.session.execute(query, {"start_date": start_date, "end_date": end_date})

    return results


def dq_download_subnational_data_csv(start_date: str, end_date: str, indicators: list[str] | None = None):
    start_date = start_date + "-01"
    end_date = end_date + "-01"
    query = text(
        """
        SELECT s.*, n.name_1 as region_name
            FROM subnational_indicators s
            INNER JOIN (
                SELECT DISTINCT ON (gid_1) gid_1, name_1 
                FROM subnational_names
            ) n 
            ON s.gid_1 = n.gid_1
            WHERE s.date BETWEEN :start_date AND :end_date;
        """
    )
    results = db.session.execute(query, {"start_date": start_date, "end_date": end_date})

    return results