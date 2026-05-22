"""
Summary Tables

Contents:
- Station Activities
- Stop Visits
- Trips Performed

"""

import dataframely as dy
import polars as pl


class StationActivities_Schema(dy.Schema):
    """
    Summarized transactions, entries, and exits by stop or station and time period for each service date (for events not associated with a trip).
    """
    service_date = dy.Date()
    stop_id = dy.String()
    time_period_start = dy.Datetime()
    time_period_end = dy.Datetime()
    time_period_category = dy.String(nullable=True)
    total_entries = dy.UInt32(nullable=True)
    total_exits = dy.UInt32(nullable=True)
    number_of_transactions = dy.UInt32(nullable=True)
    bike_entries = dy.UInt16(nullable=True)
    bike_exits = dy.UInt16(nullable=True)
    ramp_entries = dy.UInt16(nullable=True)
    ramp_exits = dy.UInt16(nullable=True)


class StopVisits_Schema(dy.Schema):
    """
    Summarized boarding, alighting, arrival, departure, and other events (kneel engaged, ramp deployed, etc.) by trip and stop for each service date.
    """
    service_date = dy.Date()
    trip_id_performed = dy.String()
    trip_stop_sequence = dy.UInt16(min=1)
    scheduled_stop_sequence = dy.UInt16(nullable=True)
    pattern_id = dy.String(nullable=True)
    vehicle_id = dy.String(nullable=True)
    dwell = dy.UInt32(nullable=True)
    stop_id = dy.String(nullable=True)
    timepoint = dy.Bool(nullable=True)
    schedule_arrival_time = dy.Datetime(nullable=True)
    schedule_departure_time = dy.Datetime(nullable=True)
    actual_arrival_time = dy.Datetime(nullable=True)
    actual_departure_time = dy.Datetime(nullable=True)
    distance = dy.UInt32(nullable=True)
    boarding_1 = dy.UInt16(nullable=True)
    alighting_1 = dy.UInt16(nullable=True)
    boarding_2 = dy.UInt16(nullable=True)
    alighting_2 = dy.UInt16(nullable=True)
    departure_load = dy.UInt16(nullable=True)
    door_open = dy.Datetime(nullable=True)
    door_close = dy.Datetime(nullable=True)
    door_status = dy.String(nullable=True)
    ramp_deployed_time = dy.Float64(nullable=True)
    ramp_failure = dy.Bool(nullable=True)
    kneel_deployed_time = dy.Float64(nullable=True)
    lift_deployed_time = dy.Float64(nullable=True)
    bike_rack_deployed = dy.Bool(nullable=True)
    bike_load = dy.UInt16(nullable=True)
    revenue = dy.Float64(nullable=True)
    number_of_transactions = dy.UInt16(nullable=True)
    schedule_relationship = dy.String(nullable=True)

    @dy.rule()
    def door_status_values(cls) -> pl.Expr:
        values = {
            "Doors did not open",
            "Front door opened and back doors remain closed",
            "Back doors opened and front door remained closed",
            "All doors opened",
            "Other configuration",
        }
        return pl.col("door_status").is_in(values)

    @dy.rule()
    def schedule_relationship_values(cls) -> pl.Expr:
        values = {"Scheduled", "Skipped", "Added", "Missing"}
        return pl.col("schedule_relationship").is_in(values)


class TripsPerformed_Schema(dy.Schema):
    """
    Trips performed for each service date.
    """
    service_date = dy.Date()
    trip_id_performed = dy.String()
    vehicle_id = dy.String()
    trip_id_scheduled = dy.String(nullable=True)
    route_id = dy.String(nullable=True)
    route_type = dy.String(nullable=True)
    ntd_mode = dy.String(nullable=True)
    route_type_agency = dy.String(nullable=True)
    shape_id = dy.String(nullable=True)
    pattern_id = dy.String(nullable=True)
    direction_id = dy.UInt8(nullable=True, min=0, max=1)
    operator_id = dy.String(nullable=True)
    block_id = dy.String(nullable=True)
    trip_start_stop_id = dy.String(nullable=True)
    trip_end_stop_id = dy.String(nullable=True)
    schedule_trip_start = dy.Datetime(nullable=True)
    schedule_trip_end = dy.Datetime(nullable=True)
    actual_trip_start = dy.Datetime(nullable=True)
    actual_trip_end = dy.Datetime(nullable=True)
    trip_type = dy.String(nullable=True)
    schedule_relationship = dy.String(nullable=True)

    @dy.rule()
    def route_type_values(cls) -> pl.Expr:
        values = {
            "Tram / Streetcar / Light rail",
            "Subway / Metro",
            "Rail",
            "Bus",
            "Ferry",
            "Cable tram",
            "Aerial lift",
            "Funicular",
            "Trolleybus",
            "Monorail",
            "Railway Service",
            "High Speed Rail Service",
            "Long Distance Trains",
            "Inter Regional Rail Service",
            "Car Transport Rail Service",
            "Sleeper Rail Service",
            "Regional Rail Service",
            "Tourist Railway Service",
            "Rail Shuttle (Within Complex)",
            "Suburban Railway",
            "Replacement Rail Service",
            "Special Rail Service",
            "Lorry Transport Rail Service",
            "All Rail Services",
            "Cross-Country Rail Service",
            "Vehicle Transport Rail Service",
            "Rack and Pinion Railway",
            "Additional Rail Service",
            "Coach Service",
            "International Coach Service",
            "National Coach Service",
            "Shuttle Coach Service",
            "Regional Coach Service",
            "Special Coach Service",
            "Sightseeing Coach Service",
            "Tourist Coach Service",
            "Commuter Coach Service",
            "All Coach Services",
            "Urban Railway Service",
            "Metro Service",
            "Underground Service",
            "All Urban Railway Services",
            "Bus Service",
            "Regional Bus Service",
            "Express Bus Service",
            "Stopping Bus Service",
            "Local Bus Service",
            "Night Bus Service",
            "Post Bus Service",
            "Special Needs Bus",
            "Mobility Bus Service",
            "Mobility Bus for Registered Disabled",
            "Sightseeing Bus",
            "Shuttle Bus",
            "School Bus",
            "School and Public Service Bus",
            "Rail Replacement Bus Service",
            "Demand and Response Bus Service",
            "All Bus Services",
            "Trolleybus Service",
            "Tram Service",
            "City Tram Service",
            "Local Tram Service",
            "Regional Tram Service",
            "Sightseeing Tram Service",
            "Shuttle Tram Service",
            "All Tram Services",
            "Water Transport Service",
            "Air Service",
            "Ferry Service",
            "Aerial Lift Service",
            "Telecabin Service",
            "Cable Car Service",
            "Elevator Service",
            "Chair Lift Service",
            "Drag Lift Service",
            "Small Telecabin Service",
            "All Telecabin Services",
            "Funicular Service",
            "Taxi Service",
            "Communal Taxi Service",
            "Water Taxi Service",
            "Rail Taxi Service",
            "Bike Taxi Service",
            "Licensed Taxi Service",
            "Private Hire Service Vehicle",
            "All Taxi Services",
            "Miscellaneous Service",
            "Horse-drawn Carriage",
        }
        return pl.col("route_type").is_in(values)

    @dy.rule()
    def ntd_mode_values(cls) -> pl.Expr:
        values = {
            "Aerial Tramway",
            "Alaska Railroad",
            "Bus",
            "Bus Rapid Transit",
            "Cable Car",
            "Commuter Bus",
            "Commuter Rail",
            "Demand Response",
            "Demand Taxi",
            "Ferryboat",
            "Heavy Rail",
            "Hybrid Rail",
            "Inclined Plane",
            "Jitney",
            "Light Rail",
            "Monorail/Automated Guideway",
            "Other",
            "Público",
            "Streetcar",
            "Trolleybus",
            "Vanpool",
        }
        return pl.col("ntd_mode").is_in(values)

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
            "Other not in service",
        }
        return pl.col("trip_type").is_in(values)

    @dy.rule()
    def schedule_relationship_values(cls) -> pl.Expr:
        values = {"Scheduled", "Added", "Unscheduled", "Canceled", "Duplicated"}
        return pl.col("schedule_relationship").is_in(values)
