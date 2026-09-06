"""Support for Google Maps popular times sensors."""
from datetime import datetime, timedelta
import logging

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import CONF_ADDRESS, CONF_NAME
import homeassistant.helpers.config_validation as cv
import livepopulartimes
import voluptuous as vol

from .const import CONF_UNIQUE_ID, unique_id_from_address

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Required(CONF_ADDRESS): cv.string,
        vol.Optional(CONF_UNIQUE_ID): cv.string,
    }
)

SCAN_INTERVAL = timedelta(minutes=10)


def setup_platform(hass, config, add_entities, discovery_info=None):
    name = config['name']
    address = config['address']
    unique_id = config.get(CONF_UNIQUE_ID)
    add_entities([PopularTimesSensor(name, address, unique_id)], True)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Popular Times sensors from a config entry."""
    async_add_entities(
        [
            PopularTimesSensor(
                entry.data[CONF_NAME],
                entry.data[CONF_ADDRESS],
                entry.unique_id,
            )
        ],
        True,
    )


class PopularTimesSensor(SensorEntity):

    def __init__(self, name, address, unique_id=None):
        self._name = name
        self._address = address
        self._attr_unique_id = unique_id or unique_id_from_address(address)
        self._attr_available = True
        self._state = None
        self._last_error = None

        self._attributes = {
            'maps_name': None,
            'address': None,
            'popularity_is_live': None,
            'last_error': None,
            'popularity_monday': None,
            'popularity_tuesday': None,
            'popularity_wednesday': None,
            'popularity_thursday': None,
            'popularity_friday': None,
            'popularity_saturday': None,
            'popularity_sunday': None,
        }

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def available(self):
        """Return if the sensor data is available."""
        return self._attr_available

    @property
    def state_class(self):
        """Return the state class of the sensor."""
        return "measurement"

    @property
    def unit_of_measurement(self):
        return '%'

    @property
    def state_attributes(self):
        return self._attributes

    def _set_available(self):
        """Mark the sensor as available and clear the last error."""
        if self._last_error is not None:
            _LOGGER.info("Recovered Popular Times data for %s", self._name)

        self._attr_available = True
        self._attributes['last_error'] = None
        self._last_error = None

    def _set_unavailable(self, error):
        """Mark the sensor unavailable and log new failures once."""
        error_message = str(error)
        self._attr_available = False
        self._state = None
        self._attributes['popularity_is_live'] = None
        self._attributes['last_error'] = error_message

        if error_message != self._last_error:
            _LOGGER.warning(
                "Unable to update Popular Times data for %s: %s",
                self._name,
                error_message,
            )
            self._last_error = error_message

    def _validate_result(self, result):
        """Validate the response returned by the popular times library."""
        if not isinstance(result, dict):
            raise ValueError("no place found for configured address")

        popular_times = result.get("populartimes")
        if not isinstance(popular_times, list) or len(popular_times) < 7:
            raise ValueError("place does not include weekly popularity data")

        for day in popular_times[:7]:
            if not isinstance(day, dict):
                raise ValueError("place includes invalid popularity data")

            data = day.get("data")
            if not isinstance(data, list) or len(data) < 24:
                raise ValueError("place does not include hourly popularity data")

    def update(self):
        """Get the latest data from Google Places API."""
        try:
            result = livepopulartimes.get_populartimes_by_address(self._address)
            self._validate_result(result)
            popularity = result.get('current_popularity', 0)

            self._attributes['address'] = result.get("address")
            self._attributes['maps_name'] = result.get("name")
            self._attributes['popularity_monday'] = result["populartimes"][0]["data"]
            self._attributes['popularity_tuesday'] = result["populartimes"][1]["data"]
            self._attributes['popularity_wednesday'] = result["populartimes"][2]["data"]
            self._attributes['popularity_thursday'] = result["populartimes"][3]["data"]
            self._attributes['popularity_friday'] = result["populartimes"][4]["data"]
            self._attributes['popularity_saturday'] = result["populartimes"][5]["data"]
            self._attributes['popularity_sunday'] = result["populartimes"][6]["data"]

            dt = datetime.now()
            weekdayIndex = dt.weekday()
            hourIndex = dt.hour
            historicalDataForWeekday = result["populartimes"][weekdayIndex]["data"]
            historicalDataForHour = historicalDataForWeekday[hourIndex]

            if popularity is not None:
                self._attributes['popularity_is_live'] = True

            if popularity is None:
                popularity = historicalDataForHour
                self._attributes['popularity_is_live'] = False
                _LOGGER.debug("Current popularity info is not live but based on historical data.")

            self._state = popularity
            self._set_available()

        except Exception as err:
            self._set_unavailable(err)
