# Changelog - Audio_Transcription Tool - 

All notable changes to this project will be documented in this file.

The format is loosely based on Keep a Changelog.

---

## [0.1.0] - 2026-02-28

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