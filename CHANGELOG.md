# Changelog

## Unreleased

- Validate UI setup addresses against the place resolved by Google Maps.
- Show the resolved place name and address before creating an entity.
- Allow resolved places to be added even when popularity data cannot be retrieved during setup.
- Store the resolved place query for future updates and use the Google place ID for stable unique IDs when available.
- Add English and Dutch setup translations, including clearer wording for temporary popularity lookup failures.
- Add debug logging for the Google Maps parser shape used by the popularity lookup.
- Mark sensors unavailable when a place cannot be found or does not return popularity data, while reducing repeated log noise.

## 0.30

- Add Home Assistant UI setup through a config flow.
- Add stable entity unique IDs so sensor settings can be managed from the UI.
- Keep existing YAML sensor configuration working, with optional `unique_id` support.
- Add HACS custom repository install documentation and repository metadata.
- Add development and release instructions for publishing HACS-visible updates.
- Add lightweight CI validation for Python and JSON files.
