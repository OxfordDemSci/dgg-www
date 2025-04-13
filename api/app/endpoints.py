from functools import wraps
import csv
from datetime import datetime
import io
import time

from flask import Blueprint, make_response, Response, request, jsonify, current_app
from flask_jwt_extended import (create_access_token, decode_token, get_jwt,
                                get_jwt_identity, jwt_required)
from sqlalchemy import or_, text, and_, insert
from .data_queries import (
    dq_get_init_data,
    dq_query_specific_country,
    dq_query_specific_region,
    dq_query_national_data,
    dq_query_subnational_data,
    dq_download_national_data_with_dates,
    dq_download_subnational_data_with_dates,
    dq_get_ground_truth_subnational,
    dq_get_ground_truth_national,
    get_user,
    dq_download_national_data_csv,
    dq_download_subnational_data_csv,
    dq_query_outcomes_by_date,
)

from .models import SubNationalIndicators, NationalIndicators
from .datatypes import Level
from .validation import validate_request_params, validate_post_requests, validate_delete_requests
from app import db

api_bp = Blueprint('api/v2', __name__)


def check_scope(required_scope):
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            claims = get_jwt()
            user_scopes = claims["scope"]

            scope_hierarchy = ["delete", "read", "write"]
            if scope_hierarchy.index(user_scopes) >= scope_hierarchy.index(
                required_scope
            ):
                return f(*args, **kwargs)
            else:
                return "You don't have permission to access this resource", 403

        return decorated_function

    return decorator


def check_delete_scope(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        claims = get_jwt()
        username = claims["sub"]  # Assuming the username is stored in the 'sub' claim

        user = get_user(username)
        if user and user.role.value == "delete":
            return f(*args, **kwargs)
        else:
            return "You don't have permission to access this resource", 403

    return decorated_function


def decodetoken(token):
    decoded_token = decode_token(token)
    return decoded_token


@api_bp.route('/login', methods=['POST'])
def login():
    from app import bcrypt

    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"message": "Missing username or password"}), 400

        user = get_user(username)
        if not user or not bcrypt.check_password_hash(user.password, password):
            return jsonify({"message": "Invalid username or password"}), 401
        additional_claims = {"scope": user.role.value}
        access_token = create_access_token(
            identity=username, additional_claims=additional_claims
        )
    except Exception as e:
        current_app.logger.error(e)
        return make_response("An error occurred while fetching the data", 500)
    return jsonify(access_token=access_token), 200


cache = {
    "data": None,
    "timestamp": 0
}
CACHE_DURATION = 60 * 60  # Cache duration in seconds (e.g., 1 hr)


def init_data() -> Response:
    try:
        current_time = time.time()
        if cache["data"] is None or (current_time - cache["timestamp"]) > CACHE_DURATION:
            # Cache is empty or expired, fetch new data
            cache["data"] = dq_get_init_data()
            cache["timestamp"] = current_time
        
        response = cache["data"]
        return make_response(response, 200)
    except Exception as e:
        return make_response({"error": str(e)}, 500)


def get_subnational_geometries() -> Response:
    try:
        response = current_app.config["SUBNATIONAL_GEOMS"]
        return make_response(response, 200)
    except Exception as e:
        return make_response({"error": str(e)}, 500)


def get_national_geometries() -> Response:
    try:
        response = current_app.config["NATIONAL_GEOMS"]
        return make_response(response, 200)
    except Exception as e:
        return make_response({"error": str(e)}, 500)


@validate_request_params
def valid_outcomes_by_date(date: str) -> Response:
    try:
        results = dq_query_outcomes_by_date(date)
    except Exception as e:
        return make_response({"error": str(e)}, 500)
    return make_response(results, 200)

@validate_request_params
def query_specific_country(country: str, indicators: list[str] | None = None) -> Response:
    try:
        results = dq_query_specific_country(country, indicators)
    except Exception as e:
        return make_response({"error": str(e)}, 500)
    return make_response(results, 200)


@validate_request_params
def query_specific_region(region: str, indicators: list[str] | None = None) -> Response:
    try:
        results = dq_query_specific_region(region, indicators)
    except Exception as e:
        return make_response({"error": str(e)}, 500)
    return make_response(results, 200)


@validate_request_params
def get_national_data(date: str, indicators: list[str] | None = None) -> Response:
    try:
        results = dq_query_national_data(date, indicators)
    except Exception as e:
        return make_response({"error": str(e)}, 500)
    return make_response(results, 200)


@validate_request_params
def get_subnational_data(date: str, country: str | None = None, indicators: list[str] | None = None) -> Response:
    try:
        results = dq_query_subnational_data(date, country, indicators)
    except Exception as e:
        return make_response({"error": str(e)}, 500)
    return make_response(results, 200)


@validate_request_params
def download_national_data_with_dates(start_date: str, end_date: str, country: str | None = None) -> Response:
    try:
        results = dq_download_national_data_with_dates(start_date, end_date, country)
    except Exception as e:
        return make_response({"error": str(e)}, 500)
    return make_response(results, 200)


@validate_request_params
def download_subnational_data_with_dates(start_date: str, end_date: str, region: str | None = None) -> Response:
    try:
        results = dq_download_subnational_data_with_dates(start_date, end_date, region)
    except Exception as e:
        return make_response({"error": str(e)}, 500)
    return make_response(results, 200)


@validate_request_params
def get_ground_truth_subnational(indicators: list[str] | None = None) -> Response:
    try:
        results = dq_get_ground_truth_subnational(indicators)
    except Exception as e:
        return make_response({"error": str(e)}, 500)
    return make_response(results, 200)


@validate_request_params
def get_ground_truth_national(indicators: list[str] | None = None) -> Response:
    try:
        results = dq_get_ground_truth_national(indicators)
    except Exception as e:
        return make_response({"error": str(e)}, 500)
    return make_response(results, 200)


@validate_request_params
def download_csv(level: Level, start_date: str, end_date: str) -> Response:
    try:
        if level == Level.NATIONAL.value:
            results = dq_download_national_data_csv(start_date, end_date)
        elif level == Level.SUBNATIONAL.value:
            results = dq_download_subnational_data_csv(start_date, end_date)
    except Exception as e:
        return make_response({"error": str(e)}, 500)
    
    def generate():
        output = io.StringIO()
        if level == Level.NATIONAL.value:
            fieldnames = ["country", "gid_0", "date", "outcome", "predicted", "predicted_error"]
        else:
            fieldnames = ["country", "gid_0", "gid_1", "region_name", "date", "outcome", "predicted", "predicted_error"]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        yield output.getvalue()
        output.seek(0)
        output.truncate(0)
        
        chunk_size = 1000  # Adjust the chunk size as needed
        chunk = []
        for row in results:
            formatted_date = row.date.strftime("%Y-%m")
            if level == Level.NATIONAL.value:
                chunk.append({
                    "country": row.country,
                    "gid_0": row.gid_0,
                    "date": formatted_date,
                    "outcome": row.outcome,
                    "predicted": round(float(row.predicted), 3) if row.predicted else None,
                    "predicted_error": round(float(row.predicted_error), 3) if row.predicted_error else None
                })
            else:
                chunk.append({
                    "country": row.country,
                    "gid_0": row.gid_0,
                    "gid_1": row.gid_1 if row.gid_1 else "NA",
                    "region_name": row.region_name if row.region_name else "NA",
                    "date": formatted_date,
                    "outcome": row.outcome,
                    "predicted": round(float(row.predicted), 3) if row.predicted else None,
                    "predicted_error": round(float(row.predicted_error), 3) if row.predicted_error else None
                })
            if len(chunk) >= chunk_size:
                writer.writerows(chunk)
                yield output.getvalue()
                output.seek(0)
                output.truncate(0)
                chunk = []
        
        # Write any remaining rows in the last chunk
        if chunk:
            writer.writerows(chunk)
            yield output.getvalue()
            output.seek(0)
            output.truncate(0)

    filename = f"{level}_data_{start_date}_to_{end_date}.csv"
    response = Response(generate(), mimetype="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-Type"] = "text/csv"
    return response


@check_scope("write")
@validate_post_requests
def post_national_data() -> Response:
    try:
        data_list = request.get_json()

        # Prepare the data for bulk insert
        records = [
            {
                'gid_0': data['gid_0'],
                'country': data['country'],
                'outcome': data['outcome'],
                'predicted': data.get('predicted'),
                'predicted_error': data.get('predicted_error'),
                'date': data['date']
            }
            for data in data_list
        ]

        # Perform a bulk insert operation using SQLAlchemy core insert statement
        stmt = insert(NationalIndicators).values(records)
        db.session.execute(stmt)

        db.session.commit()
        return make_response({"message": "Successfully posted data"}, 200)
    except Exception as e:
        db.session.rollback()
        return make_response({"error": str(e)}, 500)


@check_scope("write")
@validate_post_requests
def post_subnational_data() -> Response:
    try:
        data_list = request.get_json()

        # Prepare the data for bulk insert
        records = [
            {
                'gid_0': data['gid_0'],
                'gid_1': data['gid_1'],
                'country': data['country'],
                'outcome': data['outcome'],
                'predicted': data.get('predicted'),
                'predicted_error': data.get('predicted_error'),
                'date': data['date']
            }
            for data in data_list
        ]

        # Perform a bulk insert operation using SQLAlchemy core insert statement
        stmt = insert(SubNationalIndicators).values(records)
        db.session.execute(stmt)

        db.session.commit()
        return make_response({"message": "Successfully posted data"}, 200)
    except Exception as e:
        db.session.rollback()
        return make_response({"error": str(e)}, 500)


@check_delete_scope
#@validate_delete_requests
def delete_national_data() -> Response:
    try:
        data_list = request.get_json()

        # Extract unique values for each column
        gid_0_set = {data['gid_0'] for data in data_list}
        country_set = {data['country'] for data in data_list}
        outcome_set = {data['outcome'] for data in data_list}
        date_set = {data['date'] for data in data_list}

        # Perform a bulk delete operation using the IN clause
        db.session.query(NationalIndicators).filter(
            and_(
                NationalIndicators.gid_0.in_(gid_0_set),
                NationalIndicators.country.in_(country_set),
                NationalIndicators.outcome.in_(outcome_set),
                NationalIndicators.date.in_(date_set)
            )
        ).delete(synchronize_session=False)
        
        db.session.commit()
        return make_response({"message": "Successfully deleted data"}, 200)
    except Exception as e:
        db.session.rollback()
        return make_response({"error": str(e)}, 500)

@check_delete_scope
#@validate_delete_requests
def delete_subnational_data() -> Response:
    try:
        data_list = request.get_json()

        # Extract unique values for each column
        gid_0_set = {data['gid_0'] for data in data_list}
        gid_1_set = {data['gid_1'] for data in data_list}
        country_set = {data['country'] for data in data_list}
        outcome_set = {data['outcome'] for data in data_list}
        date_set = {data['date'] + "-01" for data in data_list}

        query = text(
            """
            DELETE FROM subnational_indicators
            WHERE gid_1 IN :gid_1_set AND
            outcome IN :outcome_set AND
            date IN :date_set
            """
        )
        db.session.execute(
            query,
            {
                "gid_1_set": tuple(gid_1_set),
                "outcome_set": tuple(outcome_set),
                "date_set": tuple(date_set)
            }
        )
        
        db.session.commit()
        return make_response({"message": "Successfully deleted data"}, 200)
    except Exception as e:
        db.session.rollback()
        return make_response({"error": str(e)}, 500)
