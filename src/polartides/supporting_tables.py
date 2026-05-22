"""
Supporting Tables

Contents:
- Devices
- Operators
- Train Cars
- Vehicle Train Cars
- Vehicles

"""

import dataframely as dy
import polars as pl


class Devices_Schema(dy.Schema):
    """
    Measurement devices, such as AVL, APC, and AFC devices, associated with vehicles or stops or stations.
    """
    device_id = dy.String()
    stop_id = dy.String(nullable=True)
    vehicle_id = dy.String(nullable=True)
    train_car_id = dy.String(nullable=True)
    device_type = dy.String(nullable=True)
    device_vendor = dy.String(nullable=True)
    device_model = dy.String(nullable=True)
    device_location = dy.String(nullable=True)

    @dy.rule()
    def device_type_values(cls) -> pl.Expr:
        values = {
            "Farebox",
            "Fare gate",
            "Fare vending machine",
            "Passenger counter",
            "Vehicle location",
            "Other",
        }
        return pl.col("device_type").is_in(values)


class Operators_Schema(dy.Schema):
    """Personnel who operate vehicles."""
    operator_id = dy.String()


class TrainCars_Schema(dy.Schema):
    """
    Assets that comprise vehicles, such as train cars, with descriptive information.
    """
    train_car_id = dy.String()
    model_name = dy.String(nullable=True)
    facility_name = dy.String(nullable=True)
    capacity_seated = dy.UInt16(nullable=True)
    capacity_wheelchair = dy.UInt16(nullable=True)
    capacity_bike = dy.UInt16(nullable=True)
    bike_rack = dy.Bool(nullable=True)
    capacity_standing = dy.UInt16(nullable=True)
    train_car_type = dy.String(nullable=True)

    @dy.rule()
    def train_car_type_values(cls) -> pl.Expr:
        values = {"Train car", "Trolley", "Other"}
        return pl.col("train_car_type").is_in(values)


class VehicleTrainCars_Schema(dy.Schema):
    """
    Relationships between assets and vehicles.
    """
    vehicle_id = dy.String()
    train_car_id = dy.String()
    train_car_order = dy.UInt16(nullable=True)
    operator_id = dy.String(nullable=True)


class Vehicles_Schema(dy.Schema):
    """
    Vehicles, including buses and train consists, with descriptive information.
    """
    vehicle_id = dy.String()
    vehicle_start = dy.Datetime(nullable=True)
    vehicle_end = dy.Datetime(nullable=True)
    model_name = dy.String(nullable=True)
    facility_name = dy.String(nullable=True)
    capacity_seated = dy.UInt16(nullable=True)
    capacity_wheelchair = dy.UInt16(nullable=True)
    capacity_bike = dy.UInt16(nullable=True)
    bike_rack = dy.Bool(nullable=True)
    capacity_standing = dy.UInt16(nullable=True)
