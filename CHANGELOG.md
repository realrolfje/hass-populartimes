# Changelog

## Unreleased

- Mark sensors unavailable when a place cannot be found or does not return popularity data.
- Reduce repeated log noise for unchanged lookup failures.

## 0.30

- Add Home Assistant UI setup through a config flow.
- Add stable entity unique IDs so sensor settings can be managed from the UI.
- Keep existing YAML sensor configuration working, with optional `unique_id` support.
- Add HACS custom repository install documentation and repository metadata.
- Add development and release instructions for publishing HACS-visible updates.
- Add lightweight CI validation for Python and JSON files.
