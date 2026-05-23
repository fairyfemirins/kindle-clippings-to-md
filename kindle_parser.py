"""
Parse Kindle 'My Clippings.txt' into structured data (Markdown, JSON).
Supports multi-language metadata (English, Chinese, Japanese).
"""

import re
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Regex for parsing Kindle clippings metadata
METADATA_REGEX = re.compile(
    r'^(.*?)(?: \((.*?)\))?(?: \| (?:Location|位置) (\d+)(?:-\d+)?(?: \| Added on )?(.*?))?$'
)

# SQLite schema for deduplication
SQL_SCHEMA = """
CREATE TABLE IF NOT EXISTS highlights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_title TEXT NOT NULL,
    author TEXT,
    content TEXT NOT NULL UNIQUE,
    location TEXT,
    timestamp DATETIME
);
"""

def parse_clippings(input_file: str, output_file: str) -> None:
    """Parse Kindle clippings and export to Markdown."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.executescript(SQL_SCHEMA)

    with open(input_file, "r", encoding="utf-8-sig") as f:
        content = f.read()

    entries = content.split("==========")
    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue

        lines = entry.split("\n")
        if len(lines) < 3:
            continue

        # Parse metadata (line 1)
        metadata = lines[0].strip()
        match = METADATA_REGEX.match(metadata)
        if not match:
            continue

        book_title, author, location, timestamp = match.groups()
        highlight = "\n".join(lines[2:]).strip()

        # Skip if highlight is empty
        if not highlight:
            continue

        # Deduplicate
        try:
            cursor.execute(
                "INSERT INTO highlights (book_title, author, content, location, timestamp) VALUES (?, ?, ?, ?, ?)",
                (book_title, author, highlight, location, timestamp)
            )
        except sqlite3.IntegrityError:
            continue  # Skip duplicates

    # Export to Markdown
    export_to_markdown(cursor, output_file)
    conn.close()

def export_to_markdown(cursor: sqlite3.Cursor, output_file: str) -> None:
    """Export highlights to Markdown with metadata."""
    cursor.execute("SELECT book_title, author, content, location, timestamp FROM highlights ORDER BY book_title")
    highlights = cursor.fetchall()

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Kindle Highlights\n\n")
        current_book = None

        for book_title, author, content, location, timestamp in highlights:
            if book_title != current_book:
                if current_book is not None:
                    f.write("\n")
                f.write(f"## {book_title}")
                if author:
                    f.write(f" ({author})")
                f.write("\n\n")
                current_book = book_title

            f.write(f"> {content}\n\n")
            if location:
                f.write(f"- *Location {location}*\n")
            if timestamp:
                try:
                    dt = datetime.strptime(timestamp, "%A, %B %d, %Y %I:%M:%S %p")
                    f.write(f"- *Added on {dt.strftime('%Y-%m-%d %H:%M:%S')}*\n")
                except ValueError:
                    pass
            f.write("\n")