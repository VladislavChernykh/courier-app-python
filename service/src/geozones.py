from datetime import datetime
from typing import Optional

from faunadb import query as q
from shapely.geometry import Point, Polygon

from service.src.common import get_client


def add_geozone(name: str, coordinates: list[tuple[float, float]]) -> dict:
    """Add geozone by name and coordinates"""
    client = get_client()
    result = client.query(
        q.create(q.collection("geozones"), {"data": dict(name=name, coordinates=list(coordinates))})
    )

    return result


def set_zone_to_courier_bond(courier_id: int, geozone_id: int) -> dict:
    """Set a zone to courier dependency with a short TTL"""
    client = get_client()
    result = client.query(
        q.create(q.collection("zone_to_courier"), {
            "data": {
                "zone_id": geozone_id,
                "courier_id": courier_id,
                "timestamp": datetime.now().timestamp()
            }})
    )

    return result


def get_delivery_data_by_coordinates(point_coordinates: [float, float]) -> dict:
    """Find an available courier and return geozone id"""
    client = get_client()
    all_geozones = client.query(
        q.map_(
            q.lambda_("x", q.get(q.var("x"))),
            q.paginate(q.match(q.index('all_geozones'))),
        )
    )
    available_geozone_id = _get_available_geozone_id(point_coordinates, all_geozones["data"])
    if not available_geozone_id:
        raise ValueError("No available geozone was found")

    geozone_to_courier_map = client.query(
        q.get(q.match(q.index("all_geozones"), available_geozone_id))
    )
    available_courier_id = geozone_to_courier_map["ref"].value["courier_id"] if geozone_to_courier_map else None

    return dict(courier_id=available_courier_id, geozone_id=available_geozone_id)


def _get_available_geozone_id(point_coordinates: [float, float], all_geozones: any) -> Optional[int]:
    """Find an available geozone id"""
    point = Point(point_coordinates)
    for geozone in all_geozones:
        geozone_id = geozone["ref"].value["id"]
        coords = geozone["data"]["coordinates"]
        if len(coords) < 3:
            print(f'Not enough coordinates for a geozone id {geozone_id}.')
            continue

        polygon = Polygon(coords)
        if point.within(polygon):
            return geozone_id
    return None
