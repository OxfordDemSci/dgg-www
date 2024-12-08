from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Enum, Integer, String, Float, Date, Boolean, TypeDecorator
from geoalchemy2 import Geometry
from datetime import datetime

from .datatypes import UserRoleEnum

import app

Base = declarative_base()


class YearMonthType(TypeDecorator):
    impl = Date

    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            if isinstance(value, str):
                value = datetime.strptime(value, '%Y-%m')
            return value.replace(day=1)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return value.strftime('%Y-%m')
        return value


class User(Base):  # type: ignore
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    role: Column[Enum] = Column(Enum(UserRoleEnum), nullable=False)

    def __init__(self, username, password=None, role=None):
        self.username = username
        if password:
            self.password = app.bcrypt.generate_password_hash(password).decode()
        self.role = role


class NationalIndicators(Base):  # type: ignore
    __tablename__ = "national_indicators"

    id = Column(Integer, primary_key=True, autoincrement=True)
    gid_0 = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    outcome = Column(String(255), nullable=False)
    predicted = Column(Float)
    predicted_error = Column(Float)
    date = Column(YearMonthType, nullable=False)


class SubNationalIndicators(Base):  # type: ignore
    __tablename__ = "subnational_indicators"

    id = Column(Integer, primary_key=True, autoincrement=True)
    gid_0 = Column(String(255), nullable=False)
    gid_1 = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    outcome = Column(String(255), nullable=False)
    predicted = Column(Float)
    predicted_error = Column(Float)
    date = Column(YearMonthType, nullable=False)


class NationalGeomeries(Base):  # type: ignore
    __tablename__ = "national_geometries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fid = Column(Integer, nullable=False)
    gid_0 = Column(String(255), nullable=False)
    geom: Geometry = Column(Geometry("MULTIPOLYGON", srid=4326), nullable=False)


class SubNationalGeometries(Base):  # type: ignore
    __tablename__ = "subnational_geometries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fid = Column(Integer, nullable=False)
    gid_0 = Column(String(255), nullable=False)
    gid_1 = Column(String(255), nullable=False)
    name_1 = Column(String(255), nullable=False)
    is_subnational = Column(Boolean, nullable=False)
    geom: Geometry = Column(Geometry("MULTIPOLYGON", srid=4326), nullable=False)


class NationalGroundTruth(Base):  # type: ignore
    __tablename__ = "national_ground_truth"

    id = Column(Integer, primary_key=True, autoincrement=True)
    gid_0 = Column(String(255), nullable=False)
    survey_year = Column(Integer, nullable=False)
    source = Column(String(255), nullable=False)
    outcome = Column(String(255), nullable=False)
    observed = Column(Float)


class SubNationalGroundTruth(Base):  # type: ignore
    __tablename__ = "subnational_ground_truth"

    id = Column(Integer, primary_key=True, autoincrement=True)
    gid_1 = Column(String(255), nullable=False)
    gid_0 = Column(String(255), nullable=False)
    survey_year = Column(Integer, nullable=False)
    outcome = Column(String(255), nullable=False)
    observed = Column(Float)
    source = Column(String(255), nullable=False)


class SubNationalNames(Base):  # type: ignore
    __tablename__ = "subnational_names"

    id = Column(Integer, primary_key=True, autoincrement=True)
    gid_0 = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    gid_1 = Column(String(255), nullable=False)
    name_1 = Column(String(255), nullable=False)


class DGGIndicatorDescription(Base):  # type: ignore
    __tablename__ = 'indicator_descriptions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    indicator_type = Column(String, nullable=False)
    mobile_women_description = Column(String(255), nullable=False)
    mobile_women_name = Column(String(255), nullable=False)
    mobile_men_description = Column(String(255), nullable=False)
    mobile_men_name = Column(String(255), nullable=False)
    mobile_gender_gap_description = Column(String(255), nullable=False)
    mobile_gender_gap_name = Column(String(255), nullable=False)
    internet_women_description = Column(String(255), nullable=False)
    internet_women_name = Column(String(255), nullable=False)
    internet_men_description = Column(String(255), nullable=False)
    internet_men_name = Column(String(255), nullable=False)
    internet_gender_gap_description = Column(String(255), nullable=False)
    internet_gender_gap_name = Column(String(255), nullable=False)
    data_frequency = Column(String(255), nullable=False)
    geographical_coverage = Column(String(255), nullable=False)
