# Release Notes Template

## Summary

Short description of this release.

Example:
This release improves the CLI input handling and fixes several stability issues.

---

## Added

New features introduced in this version.

* ...

---

## Changed

Changes to existing functionality.

* ...

---

## Fixed

Bug fixes.

* ...

---

## Technical

Internal improvements that do not affect the user directly.

* ...

---

## Notes

Additional information about the release.

Examples:

* configuration changes
* migration hints
* dependency updates

---

## Release Checklist

Before creating a release, ensure:

    -[ ] All changes are merged into `dev`
    -[ ] `dev` is stable and tested
    -[ ] `CHANGELOG.md` is updated under `[Unreleased]`
    -[ ] Move `[Unreleased]` entries to new version section
    -[ ] Version number updated in code (if applicable)
    -[ ] Create merge from `dev` → `main`
    -[ ] Create Git tag (e.g. `v1.0.2`)
    -[ ] Push `main` and tags to GitHub
    -[ ] Create GitHub Release using this template
