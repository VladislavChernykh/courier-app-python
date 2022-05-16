from collections import namedtuple

from flask import Blueprint, request
from pydantic import BaseModel, StrictStr

from service.src.geozones import add_geozone
from service.src.geozones import set_zone_to_courier_bond
from service.src.geozones import get_delivery_data_by_coordinates

Coordinates = namedtuple("Coordinates", ['latitude', 'longitude'])

geozones = Blueprint("geozones", __name__)


class GeozoneCreateData(BaseModel):
    name: StrictStr = None
    coordinates: list[Coordinates] = None


class CourierToDistrictMapData(BaseModel):
    courier_id: int = None
    geozone_id: int = None


@geozones.route("/add", methods=["POST"])
def add_zone():
    """Adding a geozone endpoint"""
    input_request = request.get_json()
    try:
        geozone_data = GeozoneCreateData(**input_request)
        result = add_geozone(geozone_data.name, geozone_data.coordinates)
        return result["ref"].value["id"]
    except ValueError as error:
        return str(error), 500


@geozones.route("/update", methods=["POST"])
def update_zone():
    """Updating a geozone endpoint"""
    input_request = request.get_json()
    try:
        data = CourierToDistrictMapData(**input_request)
        result = set_zone_to_courier_bond(data.courier_id, data.geozone_id)
        return result["ref"].value["id"]
    except ValueError as error:
        return str(error), 500


@geozones.route("/getAvailableCourier", methods=["POST"])
def get_available_courier():
    """Get available courier and geozone id by passing coordinates"""
    coords = request.get_json()
    try:
        return get_delivery_data_by_coordinates(coords)
    except ValueError as error:
        return str(error), 500
