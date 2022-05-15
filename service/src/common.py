import functools
import os
from urllib.parse import urlparse

from faunadb.client import FaunaClient


@functools.cache
def get_client():
    """Return a FaunaDB client"""
    secret = os.getenv("FAUNADB_SECRET")
    endpoint = os.getenv("FAUNADB_ENDPOINT") or "https://db.us.fauna.com/"

    url_parsed = urlparse(endpoint)

    return FaunaClient(
        secret=secret,
        domain=url_parsed.hostname,
        port=url_parsed.port,
        scheme=url_parsed.scheme
    )
