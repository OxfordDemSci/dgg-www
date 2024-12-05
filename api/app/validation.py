from functools import wraps
from flask import request, jsonify
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
        valid_outcomes = [
            "mobile_women",
            "internet_women",
            "internet_men",
            "mobile_fm_ratio",
            "internet_fm_ratio",
            "mobile_men"
        ]

        for data in data_list:
            gid_0 = data.get("gid_0")
            gid_1 = data.get("gid_1")
            country = data.get("country")
            outcome = data.get("outcome")
            date = data.get("date")

            if outcome not in valid_outcomes:
                invalid_rows.append(data)
                continue

            if not gid_1:
                existing_record = db.session.query(
                    NationalIndicators).filter_by(
                    gid_0=gid_0, country=country, outcome=outcome, date=date
                ).first()
            else:
                existing_record = db.session.query(
                    SubNationalIndicators).filter_by(
                    gid_0=gid_0, gid_1=gid_1, country=country, outcome=outcome, date=date
                ).first()
            if existing_record:
                invalid_rows.append(data)
        if invalid_rows:
            return jsonify({"error": f"Duplicate rows or invalid outcome names - Please delete these and try again: {invalid_rows}"}), 400
        return f(*args, **kwargs)
    return decorated_function


def validate_delete_requests(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data_list = request.get_json()
        invalid_rows = []
        
        for data in data_list:
            gid_0 = data.get("gid_0")
            gid_1 = data.get("gid_1")
            country = data.get("country")
            outcome = data.get("outcome")
            date = data.get("date")
            if not gid_1:
                existing_record = db.session.query(
                    NationalIndicators).filter_by(
                    gid_0=gid_0, country=country, outcome=outcome, date=date
                ).first()
            else:
                existing_record = db.session.query(
                    SubNationalIndicators).filter_by(
                    gid_0=gid_0, gid_1=gid_1, country=country, outcome=outcome, date=date
                ).first()
            if not existing_record:
                invalid_rows.append(data)
        if invalid_rows:
            return jsonify({"error": f"Rows not found: {invalid_rows}"}), 400
        return f(*args, **kwargs)
    return decorated_function