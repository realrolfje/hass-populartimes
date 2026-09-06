# Development

## Local validation

Run these checks before committing:

```bash
python3 -m compileall custom_components/populartimes
python3 -m json.tool hacs.json > /dev/null
python3 -m json.tool custom_components/populartimes/manifest.json > /dev/null
python3 -m json.tool custom_components/populartimes/strings.json > /dev/null
python3 -m json.tool custom_components/populartimes/translations/en.json > /dev/null
python3 -m json.tool custom_components/populartimes/translations/nl.json > /dev/null
```

## Release process

HACS detects versioned updates from GitHub Releases. A plain tag is not enough once the repository uses releases.

1. Update `custom_components/populartimes/manifest.json` and set `version` to the release version, for example `"0.30"`.
2. Update `README.md` or other documentation when the release changes install or configuration behavior.
3. Run the local validation checks from this document.
4. Commit the release changes:

```bash
git add README.md DEVELOPMENT.md hacs.json .github/workflows/ci.yml custom_components/populartimes
git commit -m "Release 0.30"
```

5. Push the default branch:

```bash
git push origin master
```

6. Confirm the `CI` workflow succeeds on GitHub.
7. Create and push a matching version tag:

```bash
git tag "v0.30"
git push origin "v0.30"
```

8. In GitHub, create a Release for the same tag, for example `v0.30`.
9. Put the user-facing changes in the GitHub Release notes.

For HACS users, the GitHub Release is the important part: HACS uses it to discover that an update is available and to show the release notes.
