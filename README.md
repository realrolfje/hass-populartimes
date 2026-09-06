# hass-populartimes
[![CI](https://github.com/realrolfje/hass-populartimes/actions/workflows/ci.yml/badge.svg)](https://github.com/realrolfje/hass-populartimes/actions/workflows/ci.yml)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![Version](https://img.shields.io/badge/dynamic/json?label=version&query=%24.version&url=https%3A%2F%2Fraw.githubusercontent.com%2Frealrolfje%2Fhass-populartimes%2Fmaster%2Fcustom_components%2Fpopulartimes%2Fmanifest.json)](https://github.com/realrolfje/hass-populartimes/releases)

[![Open your Home Assistant instance and open this repository in HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=realrolfje&repository=hass-populartimes&category=integration)

## Description
This is a custom component for Home Assistant.
The component generates a sensor which shows the current popularity for a place which can be found in Google Maps using the Places API.

Sensor attributes are also generated which indicate past popularity at each hour of the day. 

## Updated requirements

Since updating to a new fork of populartimes, a Google Places API key or Places Id is no longer required.

## Installation

### Install via HACS

If you use HACS:

1. Click the HACS button near the top of this README.
2. Confirm in Home Assistant that you want to open this repository in HACS.
3. Install the integration.
4. Restart Home Assistant.

If the button does not work, add the repository manually:

1. Open HACS in Home Assistant.
2. Go to `Integrations`.
3. Open the top-right menu and choose `Custom repositories`.
4. Enter this repository:

```text
https://github.com/realrolfje/hass-populartimes
```

5. Choose category `Integration`.
6. Click `Add`.
7. Search HACS for `Popular Times`.
8. Install the integration.
9. Restart Home Assistant.

Then add the integration through:

```text
Settings > Devices & services > Add integration > Popular Times
```

### Manual installation

Download the files as zip and put the contents of the `populartimes` folder in your Home Assistant `custom_components` folder.


## Configuration

When installed through HACS, configure the integration from the Home Assistant UI:

```text
Settings > Devices & services > Add integration > Popular Times
```

YAML configuration is still supported for existing installations:

```yaml
sensor:
  platform: populartimes
  name: 'your_sensor_name_here'
  address: 'your_address_here'
```
The address should preferably be in the following format:
"(location name) , full address, city, province/state/etc, country"

## Live vs historical data
Sometimes Google Maps does not provide live popularity data for the place you want to query.
In that case the historical data is used to set the sensor state.
To indicate this, the attribute `popularity_is_live` is set to `false`.

## Links:
[Home Assistant Community Topic](https://community.home-assistant.io/t/google-maps-places-popular-times-component/147362)

## Credits

This component uses the [LivePopularTimes](https://github.com/GrocerCheck/LivePopularTimes) library, which is a fork of the previously used [populartimes](https://github.com/m-wrzr/populartimes) library.
