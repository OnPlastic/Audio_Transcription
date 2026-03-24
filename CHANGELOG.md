# Changelog - Audio_Transcription - 

All notable changes to this project will be documented in this file.

The format is loosely based on Keep a Changelog.

## Development Notes

Build API documentation:

```bash
PYTHONPATH=src pdoc trsc \
  --docformat markdown \
  --logo assets/logo2.png \
  --logo-link https://github.com/OnPlastic/Audio_Transcription \
  --edit-url-map trsc=https://github.com/OnPlastic/Audio_Transcription/blob/main/src/trsc/ \
  --footer-text "Project on GitHub: https://github.com/OnPlastic/Audio_Transcription" \
  -o docs/api
```

## [Unreleased
]
---

## [1.0.2]

### Added

- Initial testing setup with 'pytest'
- Smoke test and first structured 'tests/' directory
- Core baseline tests for 'output.py', 'input_utils.py' and 'logging_setup.py'
- Internal testing notes and roadmap under 'docs/testing/'

### Changed

- Improved CLI prompt formatting for SSH / piped sessions (Termux - transcribe)

### Technical

- Introduced 'prompt_input()' helper to stabilize CLI input/output behavior 
  across TTY and non-TTY environments
- Replaced direct 'input(prompt)' calls in CLI utilities with controlled stdout handling
- Added repeatable baseline coverage for core CLI helper flows:
  - file writing
  - input validation and retry behavior
  - audio path decision flow
  - logging initialization

---

## [1.0.1] 

### Added
- Architecture diagram added to the API documentation
- Development dependencies file `requirements-dev.txt`

### Changed
- Improved API documentation landing page rendered from package docstring
- Updated static API documentation generated with pdoc
- Cleaned up runtime dependencies in `requirements.txt`

### Technical
- Documented API documentation build command in CHANGELOG
  
---

## [1.0.0] 

### Added
- Automatic API documentation generation using **pdoc**
- Static documentation site under `docs/`
- Project landing page rendered from package docstring
- Sidebar logo linking to the GitHub repository

### Changed
- Refactored project into proper Python package layout (`src/trsc`)
- Centralized application metadata and version handling
- Improved module documentation with structured Markdown docstrings

### Technical
- Added documentation build workflow using `pdoc`
- Introduced documentation directory structure (`docs/`, `docs/api/`)
- Cleaned repository structure and removed temporary test artifacts

### Notes
- First official **1.0 stable release**
- Project structure, CLI workflow and documentation considered stable

---

## [0.1.0] 

### Added
- Stable CLI workflow for audio transcription
- German transcription with Whisper large-v3
- Audio input from existing file or live microphone recording
- TXT export of transcription results
- Optional email delivery via Gmail SMTP
- Logging to terminal and log file

### Improved
- Retry logic for missing audio files
- Fallback to recorder if file input fails
- Cleaner CTRL+C handling
- Better project structure and modularized components

### Notes
- First stable CLI release

---

## [0.0.1] - 2026-02-05

### Added
- Initial stable baseline of the refactored repository structure
- Baseline modular project layout
- Foundation for recorder, transcription, output and mail workflow

### Notes
- Stable baseline before further structural and functional improvements