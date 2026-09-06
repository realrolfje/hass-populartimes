"""Constants for the Popular Times integration."""

import hashlib

from homeassistant.const import Platform

DOMAIN = "populartimes"
PLATFORMS = [Platform.SENSOR]

CONF_UNIQUE_ID = "unique_id"


def unique_id_from_address(address: str) -> str:
    """Return a stable unique ID for an address."""
    normalized_address = " ".join(address.casefold().split())
    digest = hashlib.sha256(normalized_address.encode("utf-8")).hexdigest()[:16]
    return f"{DOMAIN}_{digest}"


def unique_id_from_place(place_id: str | None, address: str) -> str:
    """Return a stable unique ID for a resolved place."""
    if place_id:
        return f"{DOMAIN}_{place_id}"

    return unique_id_from_address(address)
