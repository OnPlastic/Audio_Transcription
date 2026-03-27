# Contributing to Audio_Transcription

First off, thank you for considering contributing! It's people like you who make open-source tools better.

## How Can I Contribute?

### Reporting Bugs
- Check the **Issues** tab to see if the bug has already been reported.
- If not, open a new issue. Clearly describe the problem, your operating system, and the Whisper model you were using.

### Suggesting Enhancements
- Open an issue with the tag "enhancement".
- Describe the feature and why it would be useful (e.g., "Support for more audio formats" or "Cloud storage export").

### Pull Requests (PRs)
1. **Fork** the repository and create your branch from `main`.
2. **Install dependencies** (e.g., `pip install -r requirements.txt`).
3. If you've added code that should be tested, add some examples.
4. Ensure your code follows PEP 8 (Python style guide).
5. Open a Pull Request with a clear description of your changes.

## Development Setup

To work on this CLI tool, you will need:
- Python 3.x
- FFmpeg (required by Whisper)
- A valid SMTP configuration (for testing the email feature)

**Please note:** Never commit your private `.env` file or any files containing real email credentials or API keys!

## Style Guidelines
- Use descriptive variable names.
- Add comments to complex logic, especially around audio stream handling.
- Keep the CLI output clean and user-friendly.

## Code of Conduct
By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).
