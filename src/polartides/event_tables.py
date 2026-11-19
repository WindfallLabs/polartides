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
    transaction_id = dy.String(primary_key=True)
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


class DeviceEvents_Schema(dy.Schema):  # previously PassengerEvents_Schema
    """
    Timestamped device-recorded events, including boardings, alightings, fare gate passages, and mobile validator events.
    """
    device_event_id = dy.String(
        primary_key=True,
        description="Identifies the recorded device event."
    )
    service_date = dy.Date(
        description="Service date. References GTFS"
    )
    event_timestamp = dy.Datetime(
        description="Recorded event timestamp."
    )
    location_ping_id = dy.String(
        nullable=True,
        description="Identifies the vehicle location where the device event occurred"
    )
    trip_id_performed = dy.String(
        nullable=True,
        description="Identifies the trip performed. If trips_performed table is used, this must be populated in order to link to it."
    )
    trip_id_scheduled = dy.String(
        nullable=True,
        description="Identifies the scheduled trip."
    )
    trip_stop_sequence = dy.UInt16(
        min=1,
        description="The actual order of stops visited within a performed trip. The values must start at 1 and must be consecutive along the trip. Required for vehicle-based events; optional for station-based or mobile device events not associated with a trip. Example: A bus departs the first stop and detours around the second and third scheduled stops, visiting one unscheduled stop and resuming regular service at the 4th scheduled stop. The scheduled_stop_sequence is [1, null, 4], and the trip_stop_sequence is [1, 2, 3]."
    )
    scheduled_stop_sequence = dy.UInt16(
        min=0,
        description="Scheduled order of stops for a particular trip. The values must increase along the trip but do not need to be consecutive. References GTFS"
    )
    event_type = dy.String(
        description="Indicates the type of event recorded. Use passenger_boarded/passenger_alighted for vehicle boarding/alighting events. Use passenger_entry/passenger_exit for station-based events like fare gate passages."
    )
    vehicle_id = dy.String(
        description="Identifies a vehicle. Required for vehicle-mounted device events; optional for station-based or mobile device events."
    )
    device_id = dy.String(
        nullable=True,
        description="Identifies the device that recorded the event. Links to the devices table to determine device type (vehicle-mounted, station-based, or mobile)."
    )
    employee_id = dy.String(
        nullable=True,
        description="Identifies the employee operating a handheld device, such as a fare inspector or conductor with a mobile validator."
    )
    train_car_id = dy.String(
        nullable=True,
        description="Identifies the train car."
    )
    stop_id = dy.String(
        nullable=True,
        description="Identifies the stop or station where the event occurred, recorded as of the time of the event. For vehicle-mounted device events, the stop the vehicle is serving. References GTFS"
    )
    latitude = dy.Float64(
        min=-90.0,
        max=90.0,
        description="Degrees North, in the WGS-84 coordinate system. Used for mobile device events not at a fixed location."
    )
    longitude = dy.Float64(
        min=-180.0,
        max=180.0,
        description="Degrees East, in the WGS-84 coordinate system. Used for mobile device events not at a fixed location."
    )
    pattern_id = dy.String(
        nullable=True,
        description="Identifies the unique stop-path for a trip, may be distinct from GTFS shapes.shape_id"
    )
    event_count = dy.UInt16(
        min=0,
        description="Count for this event. Default is 1. Use values > 1 only for truly simultaneous events (e.g., a parent carrying a child through a doorway as a single boarding event). Aggregated APC counts (e.g., ‘6 passengers boarded at this stop’) should be recorded in stop_visits, not device_events, since device_events is intended for discrete, instantaneous events. A value of 0 indicates that the event was recorded but no passengers were counted (e.g., door opened but no one boarded), which is distinct from null/missing data."
    )

    @dy.rule()
    def event_type_values(cls) -> pl.Expr:
        values = {
            "vehicle_arrived",
            "vehicle_departed",
            "door_opened",
            "door_closed",
            "passenger_boarded",
            "passenger_alighted",
            "passenger_entry",
            "passenger_exit",
            "kneel_engaged",
            "kneel_disengaged",
            "ramp_deployed",
            "ramp_raised",
            "ramp_failed",
            "lift_deployed",
            "lift_raised",
            "bike_boarded",
            "bike_alighted",
            "bike_rack_deployed",
        }
        return pl.col("event_type").is_in(values)


class VehicleLocations_Schema(dy.Schema):
    """
    Timestamped vehicle locations and speeds.
    """
    location_ping_id = dy.String(primary_key=True)
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
