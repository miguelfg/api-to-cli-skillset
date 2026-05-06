# HTML to Markdown Parser Skill

Convert downloaded HTML articles to clean, readable Markdown with automatic metadata extraction.

## Quick Start

```bash
# Install dependencies
pip install trafilatura beautifulsoup4

# Convert all HTML files to Markdown
python scripts/html_to_markdown.py --batch ../html_copies ../markdown_articles

# Convert a single file
python scripts/html_to_markdown.py ../html_copies/article.html
```

## Files in This Skill

- **SKILL.md** - Full skill documentation and specifications
- **scripts/html_to_markdown.py** - Main conversion script (both batch and single-file modes)
- **references/USAGE_GUIDE.md** - Practical examples and workflows
- **assets/** - (empty, reserved for future templates)

## What It Does

✓ Extracts article title, author, publication date
✓ Removes ads, navigation, sidebars, comments
✓ Converts HTML to clean Markdown
✓ Batch converts entire directories
✓ Preserves formatting (lists, tables, emphasis)
✓ Keeps hyperlinks as Markdown syntax

## Key Features

- **Smart Content Detection**: Uses machine learning (trafilatura) or HTML parsing (BeautifulSoup) to identify main article
- **Metadata Extraction**: Automatically finds and includes title, author, date, source URL
- **Batch Processing**: Convert 20+ articles at once with progress tracking
- **Graceful Degradation**: Falls back to simpler extraction if advanced tools aren't available
- **Error Handling**: Continues processing if individual files fail, reports summary

## Example Output

```markdown
# Article Title

**Author:** Jane Doe
**Date:** 2026-03-12
**Source:** [nieman.org](https://example.com/article)

---

Article content here...
```

## For Your AI Journalism Research

This skill is designed to complement your `articles-index.md` and `html_copies/` collection:

1. **Index** → articles-index.md (reference list)
2. **HTML** → html_copies/ (downloaded pages)
3. **Parse** → html-to-markdown-parser (this skill)
4. **Markdown** → markdown_articles/ (readable text)
5. **Analyze** → Extract themes and findings

## Next Steps

See `references/USAGE_GUIDE.md` for:
- Detailed workflow examples
- Troubleshooting and tips
- Integration with your research process
