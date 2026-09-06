"""Config flow for the Popular Times integration."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_ADDRESS, CONF_NAME
import homeassistant.helpers.config_validation as cv

from .api import (
    NoPopularityDataError,
    PlaceNotFoundError,
    PopularTimesError,
    format_place_query,
    get_place,
    has_popularity_data,
)
from .const import DOMAIN, unique_id_from_place


class PopularTimesConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Popular Times."""

    VERSION = 1

    def __init__(self):
        """Initialize the config flow."""
        self._pending_data = None
        self._resolved_name = None
        self._resolved_address = None
        self._resolved_place_id = None
        self._popularity_available = True

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        return await self._handle_user_step("user", user_input)

    async def async_step_user_with_resolved_place(self, user_input=None):
        """Handle retry after resolving a place without popularity data."""
        return await self._handle_user_step("user", user_input)

    async def _handle_user_step(self, step_id, user_input=None):
        """Handle the user input step."""
        errors = {}
        defaults = user_input or {}
        description_placeholders = None

        if user_input is not None:
            try:
                result = await self.hass.async_add_executor_job(
                    get_place,
                    user_input[CONF_ADDRESS],
                    False,
                )
            except PlaceNotFoundError:
                errors["base"] = "not_found"
            except NoPopularityDataError as err:
                errors["base"] = "no_popularity_data"
                if err.result:
                    resolved_query = format_place_query(err.result, user_input[CONF_ADDRESS])
                    defaults = {
                        **user_input,
                        CONF_ADDRESS: resolved_query,
                    }
                    step_id = "user_with_resolved_place"
                    description_placeholders = {
                        "name": err.result.get("name") or user_input[CONF_NAME],
                        "address": err.result.get("address") or user_input[CONF_ADDRESS],
                    }
            except PopularTimesError:
                errors["base"] = "unknown"
            except Exception:
                errors["base"] = "cannot_connect"
            else:
                self._resolved_place_id = result.get("place_id")
                self._popularity_available = has_popularity_data(result)
                await self.async_set_unique_id(
                    unique_id_from_place(
                        self._resolved_place_id,
                        user_input[CONF_ADDRESS],
                    )
                )
                self._abort_if_unique_id_configured()

                resolved_query = format_place_query(result, user_input[CONF_ADDRESS])
                self._pending_data = {
                    **user_input,
                    CONF_ADDRESS: resolved_query,
                }
                self._resolved_name = result.get("name") or user_input[CONF_NAME]
                self._resolved_address = result.get("address") or user_input[CONF_ADDRESS]

                return await self.async_step_confirm()

        data_schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default=defaults.get(CONF_NAME, "")): cv.string,
                vol.Required(CONF_ADDRESS, default=defaults.get(CONF_ADDRESS, "")): cv.string,
            }
        )

        return self.async_show_form(
            step_id=step_id,
            data_schema=data_schema,
            errors=errors,
            description_placeholders=description_placeholders,
        )

    async def async_step_confirm(self, user_input=None):
        """Confirm the resolved place before creating the config entry."""
        if self._pending_data is None:
            return await self.async_step_user()

        if user_input is not None:
            return self.async_create_entry(
                title=self._pending_data[CONF_NAME],
                data={
                    **self._pending_data,
                    "resolved_name": self._resolved_name,
                    "resolved_address": self._resolved_address,
                    "resolved_place_id": self._resolved_place_id,
                },
            )

        return self.async_show_form(
            step_id="confirm" if self._popularity_available else "confirm_without_popularity",
            data_schema=vol.Schema({}),
            description_placeholders={
                "name": self._resolved_name,
                "address": self._resolved_address,
            },
        )

    async def async_step_confirm_without_popularity(self, user_input=None):
        """Confirm a resolved place that did not include popularity data."""
        return await self.async_step_confirm(user_input)
