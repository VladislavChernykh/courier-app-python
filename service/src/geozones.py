from datetime import datetime

from faunadb import query as q

from service.src.common import get_client


def add_geozone(name: str, coordinates: list[tuple[float, float]]):
    """Add geozone by name and coordinates"""
    client = get_client()
    result = client.query(
        q.create(q.collection("geozones"), {"data": dict(name=name, coordinates=list(coordinates))})
    )

    return result


def set_zone_to_courier_bond(courier_id: int, geozone_id: int):
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
