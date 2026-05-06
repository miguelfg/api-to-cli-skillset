---
name: html-to-markdown-parser
description: Convert HTML article files to clean, readable Markdown with automatic extraction of content and metadata (title, author, date). Supports both batch conversion of entire directories and individual file processing.
---

# HTML to Markdown Parser Skill

## Purpose

This skill transforms HTML article files into clean, readable Markdown format. It automatically extracts main article content while removing navigation, ads, sidebars, and other clutter. Metadata (title, author, date) is extracted and included at the top of each Markdown file.

## When to Use

Use this skill when:
- Converting downloaded HTML articles to readable text format
- Extracting article content and metadata from web pages in bulk
- Preparing research materials for analysis or archival
- Processing news articles or journalistic content

## How to Use

### Installation

The skill includes a Python script (`scripts/html_to_markdown.py`) that requires optional dependencies for best results:

```bash
# For enhanced article extraction (highly recommended)
pip install trafilatura beautifulsoup4

# Minimum (basic functionality)
pip install beautifulsoup4
```

### Single File Conversion

To convert an individual HTML file:

```bash
python scripts/html_to_markdown.py <path/to/article.html> [output_directory]
```

Examples:
```bash
python scripts/html_to_markdown.py article.html
python scripts/html_to_markdown.py ./html_copies/new_york_times/article.html ./markdown_output
```

Output: Creates a Markdown file with the same name as the HTML input.

### Batch Conversion

To convert all HTML files in a directory recursively:

```bash
python scripts/html_to_markdown.py --batch <input_directory> [output_directory]
```

Examples:
```bash
# Convert all HTML in current directory to ./markdown
python scripts/html_to_markdown.py --batch ./html_copies

# Convert to specific output directory
python scripts/html_to_markdown.py --batch ./html_copies ./markdown_articles
```

Output: Creates a `markdown/` directory (or specified output dir) with converted `.md` files organized in the same structure as source HTML.

## What Gets Extracted

### Metadata Header
Each Markdown file starts with extracted metadata:
- **Title**: From page `<h1>`, `<title>`, or filename
- **Author**: From meta tags or byline elements
- **Date**: From publication date meta tags
- **Source**: Link back to original URL

### Content
- Main article text with intelligent removal of:
  - Navigation elements
  - Advertisements and tracking code
  - Sidebars and related content sections
  - Comments and user-generated content
  - Script and style tags

### Formatting
- Preserves paragraph breaks and structure
- Maintains text hierarchy (headings, emphasis)
- Converts lists, tables, and code blocks where applicable
- Keeps hyperlinks as Markdown syntax `[text](url)`

## Smart Extraction Logic

The script uses a layered approach for best results:

1. **Primary (Trafilatura)**: If available, uses news-optimized extraction
2. **Secondary (BeautifulSoup)**: Intelligent HTML parsing with ad/nav removal
3. **Fallback**: Simple text extraction from HTML structure

Each method attempts to identify and extract main article content while filtering out common web page clutter.

## Output Example

```markdown
# Climate Change in 2026: What Scientists Say

**Author:** Jane Smith
**Date:** 2026-03-10
**Source:** [Example News](https://example.com/article)

---

Climate scientists released a new report this week showing accelerated
warming trends. The report indicates...

[Rest of article content]
```

## Troubleshooting

**Issue: "No HTML files found"**
- Ensure HTML files are in the specified directory
- Check file extensions are `.html`

**Issue: Incomplete content extraction**
- Install trafilatura for better news article extraction: `pip install trafilatura`
- Some websites with complex structures may extract partially

**Issue: Metadata not extracted**
- Pages without standard meta tags will use filename or first heading as title
- Source URL will be recorded from input path if available

## Integration with Article Index

This skill is designed to work with the `articles-index.md` file:

1. Download HTML files using the index as reference
2. Run batch conversion on `html_copies/` directory
3. Process generated Markdown files for further analysis or archival
