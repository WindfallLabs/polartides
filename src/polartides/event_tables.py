"""
Event Tables

Contents:
- Fare Transactions
- Passenger Events
- Vehicle Locations

"""

import dataframely as dy
import polars as pl


class FareTransactions_Schema(dy.Schema):
    """
    Timestamped fare transaction, associated with devices.
    """
    transaction_id = dy.String()
    service_date = dy.Date()
    event_timestamp = dy.Datetime()
    location_ping_id = dy.String(nullable=True)
    amount = dy.Float64()
    currency_type = dy.String(nullable=True)
    fare_action = dy.String()
    trip_id_performed = dy.String(nullable=True)
    trip_id_scheduled = dy.String(nullable=True)
    pattern_id = dy.String(nullable=True)
    trip_stop_sequence = dy.UInt16(nullable=True)
    scheduled_stop_sequence = dy.UInt16(nullable=True)
    vehicle_id = dy.String(nullable=True)
    device_id = dy.String(nullable=True)
    fare_id = dy.String(nullable=True)
    stop_id = dy.String(nullable=True)
    num_riders = dy.UInt16(nullable=True)
    fare_media_id = dy.String(nullable=True)
    rider_category = dy.String(nullable=True)
    fare_product = dy.String(nullable=True)
    fare_period = dy.String(nullable=True)
    fare_capped = dy.Bool()
    token_id = dy.String(nullable=True)
    balance = dy.Float64(nullable=True)

    @dy.rule()
    def fare_action_values(cls) -> pl.Expr:
        values = {
            "Unknown action type",
            "Purchase",
            "Enter",
            "Exit",
            "Transfer entrance",
            "Transfer exit",
            "Add",
            "New",
            "Capture",
            "Extend",
            "Combine",
            "Void",
            "Activate",
            "Adjust",
            "Other",
        }
        return pl.col("fare_action").is_in(values)

    @dy.rule()
    def fare_media_id_values(cls) -> pl.Expr:
        values = {
            "Cash or coins",
            "Smart card or ticket",
            "Magnetic-stripe card or ticket",
            "Bank card",
            "Mobile NFC",
            "Optical scan",
            "Button pressed by driver or operator to indicate a boarding or alighting passenger.",
            "Other type",
        }
        return pl.col("fare_media_id").is_in(values)


class PassengerEvents_Schema(dy.Schema):
    """
    Timestamped passenger-related events, including boardings and alightings.
    """
    passenger_event_id = dy.String()
    service_date = dy.Date()
    event_timestamp = dy.Datetime()
    location_ping_id = dy.String(nullable=True)
    trip_id_performed = dy.String(nullable=True)
    trip_id_scheduled = dy.String(nullable=True)
    trip_stop_sequence = dy.UInt16()
    scheduled_stop_sequence = dy.UInt16(nullable=True)
    event_type = dy.String()
    vehicle_id = dy.String()
    device_id = dy.String(nullable=True)
    train_car_id = dy.String(nullable=True)
    stop_id = dy.String(nullable=True)
    pattern_id = dy.String(nullable=True)
    event_count = dy.UInt16(nullable=True)

    @dy.rule()
    def event_type_values(cls) -> pl.Expr:
        values = {
            "Vehicle arrived at stop",
            "Vehicle departed stop",
            "Door opened",
            "Door closed",
            "Passenger boarded",
            "Passenger alighted",
            "Kneel was engaged",
            "Kneel was disengaged",
            "Ramp was deployed",
            "Ramp was raised",
            "Ramp deployment failed",
            "Lift was deployed",
            "Lift was raised",
            "Individual bike boarded",
            "Individual bike alighted",
            "Bike rack deployed",
        }
        return pl.col("event_type").is_in(values)


class VehicleLocations_Schema(dy.Schema):
    """
    Timestamped vehicle locations and speeds.
    """
    location_ping_id = dy.String()
    service_date = dy.Date(nullable=True)
    event_timestamp = dy.Datetime()
    trip_id_performed = dy.String(nullable=True)
    trip_id_scheduled = dy.String(nullable=True)
    trip_stop_sequence = dy.UInt16(nullable=True, min=1)
    scheduled_stop_sequence = dy.UInt32(nullable=True)
    vehicle_id = dy.String()
    device_id = dy.String(nullable=True)
    pattern_id = dy.String(nullable=True)
    stop_id = dy.String(nullable=True)
    current_status = dy.String(nullable=True)
    latitude = dy.Float64(nullable=True, min=-90.0, max=90.0)
    longitude = dy.Float64(nullable=True, min=-180.0, max=180.0)
    gps_quality = dy.String(nullable=True)
    heading = dy.UInt16(min=0, max=359)
    speed = dy.UInt16()
    odometer = dy.UInt32()
    schedule_deviation = dy.Int32(nullable=True)
    headway_deviation = dy.Int32(nullable=True)
    trip_type = dy.String(nullable=True)
    schedule_relationship = dy.String(nullable=True)

    @dy.rule()
    def current_status_values(cls) -> pl.Expr:
        values = {"Incoming at", "Stopped at", "In transit to"}
        return pl.col("current_status").is_in(values)

    @dy.rule()
    def gps_quality_values(cls) -> pl.Expr:
        values = {"Excellent", "Good", "Poor"}
        return pl.col("gps_quality").is_in(values)

    @dy.rule()
    def trip_type_values(cls) -> pl.Expr:
        values = {
            "In service",
            "Deadhead",
            "Layover",
            "Pullout",
            "Pullin",
            "Extra Pullout",
            "Extra Pullin",
            "Deadhead To Layover",
            "Deadhead From Layover",
            "Other not in service"
        }
        return pl.col("trip_type").is_in(values)

    @dy.rule()
    def schedule_relationship_values(cls) -> pl.Expr:
        values = {"Scheduled", "Skipped", "Added", "Missing"}
        return pl.col("schedule_relationship").is_in(values)
