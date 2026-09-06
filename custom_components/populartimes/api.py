"""API helpers for the Popular Times integration."""

import logging

from livepopulartimes import crawler

_LOGGER = logging.getLogger(__name__)


class PopularTimesError(Exception):
    """Base error for Popular Times lookups."""


class PlaceNotFoundError(PopularTimesError):
    """Raised when the configured address does not resolve to a place."""


class NoPopularityDataError(PopularTimesError):
    """Raised when a place does not include popular times data."""

    def __init__(self, message, result=None):
        """Initialize the error."""
        super().__init__(message)
        self.result = result


def get_place(address, require_popularity=True):
    """Return validated popular times data for an address."""
    result = _get_populartimes_by_address(address)
    validate_place(result, require_popularity=require_popularity)
    return result


def format_place_query(result, fallback_address):
    """Return a specific query string for future lookups."""
    address = result.get("address") or fallback_address
    name = result.get("name")

    if name and address and name.casefold() not in address.casefold():
        return f"{name}, {address}"

    return address


def has_popularity_data(result):
    """Return whether a result includes usable hourly popularity data."""
    popular_times = result.get("populartimes") if isinstance(result, dict) else None
    if not isinstance(popular_times, list) or len(popular_times) < 7:
        return False

    for day in popular_times[:7]:
        if not isinstance(day, dict):
            return False

        data = day.get("data")
        if not isinstance(data, list) or len(data) < 24:
            return False

    return True


def validate_place(result, require_popularity=True):
    """Validate the response returned by the popular times library."""
    if not isinstance(result, dict):
        raise PlaceNotFoundError("no place found for configured address")

    if not result.get("address"):
        raise PlaceNotFoundError("no place found for configured address")

    if not require_popularity:
        return

    if not has_popularity_data(result):
        raise NoPopularityDataError("place does not include weekly popularity data", result)


def _get_populartimes_by_address(address):
    """Fetch place data and log the parser shape used by LivePopularTimes."""
    jdata = crawler.make_google_search_request(address)
    info = crawler.index_get(jdata, 0, 1, 0, 14)

    rating = crawler.index_get(info, 4, 7)
    rating_n = crawler.index_get(info, 4, 8)
    popular_times = crawler.index_get(info, 84, 0)
    current_popularity = crawler.index_get(info, 84, 7, 1)
    time_spent = crawler.index_get(info, 117, 0)
    info_84 = crawler.index_get(info, 84)

    detail = {
        "name": crawler.index_get(info, 11),
        "place_id": crawler.index_get(info, 78),
        "address": crawler.index_get(info, 39),
        "coordinates": {
            "lat": crawler.index_get(info, 9, 2),
            "lng": crawler.index_get(info, 9, 3),
        },
        "categories": crawler.index_get(info, 13),
        "place_types": crawler.index_get(info, 76),
        "current_popularity": current_popularity,
        "popular_times": popular_times,
    }

    result = crawler.add_param_from_search(
        {},
        {},
        rating,
        rating_n,
        popular_times,
        current_popularity,
        time_spent,
        detail,
    )

    _LOGGER.debug(
        (
            "Popular Times lookup: query=%r, resolved_name=%r, "
            "resolved_address=%r, place_id=%r, info_len=%s, info_84_type=%s, "
            "info_84_len=%s, has_popular_times=%s, has_current_popularity=%s"
        ),
        address,
        result.get("name"),
        result.get("address"),
        result.get("place_id"),
        len(info) if isinstance(info, list) else None,
        type(info_84).__name__,
        len(info_84) if isinstance(info_84, list) else None,
        popular_times is not None,
        current_popularity is not None,
    )

    return result
