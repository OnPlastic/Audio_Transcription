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

### Code & Stability

* [ ] All changes are merged into `dev`
* [ ] `dev` is stable and fully tested (`pytest` passes)

### Versioning & Changelog

* [ ] `CHANGELOG.md` is updated under `[Unreleased]`
* [ ] Move `[Unreleased]` entries to new version section
* [ ] Version number updated in code (e.g. `__version__`)

### Documentation & Presentation

* [ ] README(_de) badges updated (version, test status)
* [ ] Project documentation updated (if applicable)
* [ ] API docs rebuilt (pdoc) if code or docstrings changed

### Release Process

* [ ] Create release branch from `dev` (e.g. `release/vX.X.X`)
* [ ] Final checks on release branch (tests, docs)
* [ ] Merge release branch into `main`
* [ ] Create Git tag (e.g. `v1.0.3`)
* [ ] Push `main` and tags to GitHub
* [ ] Create GitHub Release using this template

### Post-Release

* [ ] Merge release changes back into `dev` (if needed)
* [ ] Clean up release/hotfix branches
