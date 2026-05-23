# Kindle Clippings to Markdown CLI

Convert Kindle's `My Clippings.txt` into structured Markdown notes with metadata (book title, author, location, timestamp).

## Features
- **Multi-Language Support**: Parses metadata in English, Chinese, Japanese.
- **Deduplication**: Skips duplicate highlights using SQLite.
- **CLI Interface**: Simple `click`-based CLI for easy integration.

## Installation
```bash
cd /home/femirins/kindle_clippings_to_md
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

## Usage
```bash
python cli.py convert My\ Clippings.txt --output highlights.md
```

## Technical Architecture
- **Regex Parsing**: Flexible regex to handle multi-language metadata.
- **SQLite Deduplication**: Ensures no duplicate highlights.
- **Markdown Export**: Structured output with book titles, authors, and timestamps.

## License
MIT