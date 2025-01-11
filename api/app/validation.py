from functools import wraps
from flask import request, jsonify
from sqlalchemy import text
from sqlalchemy.sql import bindparam
from .models import (
    SubNationalIndicators,
    NationalIndicators,
)

from .datatypes import Level

from app import db

def validate_request_params(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        country = request.args.get("country")
        region = request.args.get("region")
        indicators = request.args.getlist("indicators")
        date = request.args.get("date")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        if country:
            country_exists = db.session.query(
                db.exists().where(NationalIndicators.gid_0 == country)
            ).scalar()
            if not country_exists:
                return jsonify({"error": f"Invalid country - {country}"}), 400

        # Check if region is in SubNationalIndicators.gid_1
        if region:
            region_exists = db.session.query(
                db.exists().where(SubNationalIndicators.gid_1 == region)
            ).scalar()
            if not region_exists:
                return jsonify({"error": f"Invalid region - {region}"}), 400

        # Check if all indicators are in SubNationalIndicators.outcome
        if indicators:
            valid_indicators = db.session.query(
                SubNationalIndicators.outcome
            ).distinct().all()
            valid_indicators = {i[0] for i in valid_indicators}
            invalid_indicators = [i for i in indicators if i not in valid_indicators]
            if invalid_indicators:
                return jsonify({"error": f"Invalid indicators: {', '.join(invalid_indicators)}"}), 400
        if date:
            if not date_in_db(date, Level.NATIONAL) and not date_in_db(date, Level.SUBNATIONAL):
                return jsonify({"error": f"Invalid date {date}"}), 400
        if start_date:
            if not date_in_db(start_date, Level.NATIONAL) and not date_in_db(start_date, Level.SUBNATIONAL):
                return jsonify({"error": f"Invalid start date {start_date}"}), 400
        if end_date:
            if not date_in_db(end_date, Level.NATIONAL) and not date_in_db(end_date, Level.SUBNATIONAL):
                return jsonify({"error": "Invalid end date {end_date}"}), 400
        return f(*args, **kwargs)

    return decorated_function


def date_in_db(date, level):
    if level == Level.NATIONAL:
        date_exists = db.session.query(
            db.exists().where(NationalIndicators.date == date)
        ).scalar()
    else:
        date_exists = db.session.query(
            db.exists().where(SubNationalIndicators.date == date)
        ).scalar()
    return date_exists


def validate_post_requests(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data_list = request.get_json()
        invalid_rows = []

        set_to_check, existing_gids = get_existing_gids(data_list)

        matching_tuple = set_to_check.intersection(existing_gids)
        for match in matching_tuple:
            invalid_rows.append({
                "gid_0": match[0],
                "gid_1": match[1],
                "date": match[2][:-3],
                "country": match[3],
                "outcome": match[4]
            })

        if invalid_rows:
            return jsonify({"error": f"Duplicate rows or invalid outcome names - Please delete these and try again: {invalid_rows}"}), 400
        return f(*args, **kwargs)
    return decorated_function


def validate_delete_requests(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data_list = request.get_json()
        invalid_rows = []

        set_to_check, existing_gids = get_existing_gids(data_list)

        differing_tuple = set_to_check.difference(existing_gids)

        for match in differing_tuple:
            invalid_rows.append({
                "gid_0": match[0],
                "gid_1": match[1],
                "date": match[2][:-3],
                "country": match[3],
                "outcome": match[4]
            })
        if invalid_rows:
            return jsonify({"error": f"Rows not found: {invalid_rows}"}), 400
        return f(*args, **kwargs)
    return decorated_function


def get_existing_gids(data_list):
    # Batch process data
    gid_0_set = {data.get("gid_0") for data in data_list}
    gid_1_set = {data.get("gid_1") for data in data_list}
    country_set = {data.get("country") for data in data_list}
    outcome_set = {data.get("outcome") for data in data_list}
    date_set = {data.get("date") + "-01" for data in data_list}
    set_to_check = set([(data.get("gid_0"), data.get("gid_1"), data.get("date") + "-01", data.get("country"), data.get("outcome")) for data in data_list])

    if len(gid_1_set) > 0:
        existing_gids = db.session.execute(
            text("""
            SELECT gid_0, gid_1, date, country, outcome
            FROM subnational_indicators
            WHERE gid_0 IN :gid_0_set
            AND gid_1 IN :gid_1_set
            AND date IN :date_set
            AND outcome IN :outcome_set
            AND country IN :country_set
            """),
            {
                "gid_0_set": tuple(gid_0_set),
                "gid_1_set": tuple(gid_1_set),
                "date_set": tuple(date_set),
                "outcome_set": tuple(outcome_set),
                "country_set": tuple(country_set),
            }
        ).fetchall()
        existing_gids = {(row[0], row[1], row[2].strftime('%Y-%m-%d'), row[3], row[4]) for row in existing_gids}
    else:
        existing_gids = db.session.execute(
            text("""
            SELECT gid_0, date, country, outcome
            FROM national_indicators
            WHERE gid_0 IN :gid_0_set
            AND date IN :date_set
            AND outcome IN :outcome_set
            AND country IN :country_set
            """),
            {
                "gid_0_set": tuple(gid_0_set),
                "date_set": tuple(date_set),
                "outcome_set": tuple(outcome_set),
                "country_set": tuple(country_set),
            }
        ).fetchall()
        existing_gids = {(row[0], None, row[1].strftime('%Y-%m-%d'), row[2], row[3]) for row in existing_gids}
    return set_to_check, existing_gids
