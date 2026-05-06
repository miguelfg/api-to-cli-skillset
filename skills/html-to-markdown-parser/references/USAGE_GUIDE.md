# HTML to Markdown Parser - Usage Guide

## Quick Start

### 1. Setup Dependencies
```bash
pip install trafilatura beautifulsoup4
```

### 2. Convert Your HTML Files

For your AI journalism research project specifically:

```bash
# Convert all downloaded articles from html_copies/
python scripts/html_to_markdown.py --batch ./html_copies ./markdown_articles

# This creates:
# markdown_articles/
# ├── bellingcat/
# ├── industry_research/
# ├── lighthouse_reports/
# ├── new_york_times/
# ├── propublica/
# ├── pulitzer_center/
# └── the_guardian/
```

## Common Workflows

### Workflow 1: Convert Entire Research Collection
```bash
cd /path/to/ai/research-on-ai-usage
python html-to-markdown-parser/scripts/html_to_markdown.py --batch html_copies markdown_copies
```

Result: All HTML articles converted to readable Markdown with metadata intact.

### Workflow 2: Process Specific Outlet
```bash
# Just convert Lighthouse Reports articles
python scripts/html_to_markdown.py --batch ./html_copies/lighthouse_reports ./lighthouse_md
```

### Workflow 3: Single Article Quality Check
```bash
# Convert one article to review extraction quality
python scripts/html_to_markdown.py ./html_copies/new_york_times/article.html
# Opens: ./html_copies/new_york_times/article.md
```

## Output Quality Expectations

### High Quality Extraction
These sources typically convert excellently:
- Nieman Lab articles ✓
- Lighthouse Reports ✓
- Bellingcat ✓
- Open Society Foundations ✓
- Reuters Institute ✓
- Poynter ✓

### Known Issues
- **Pulitzer Center (403 blocked)**: Not downloaded, so no conversion available
- **Taylor & Francis (paywalled)**: Not downloaded
- **ProPublica homepage**: Will extract homepage content, not individual articles

## After Conversion

Once Markdown files are generated:

1. **Review for quality**: Check 1-2 converted files from each outlet
2. **Extract key points**: Use Markdown format for easy copy-paste to notes
3. **Create thematic index**: Group articles by topic (tools, ethics, labor, etc.)
4. **Archive**: Keep both HTML and Markdown for reference

## Integration with Research Workflow

```
1. articles-index.md (reference list)
   ↓
2. html_copies/ (downloaded HTML)
   ↓
3. html-to-markdown-parser (this skill)
   ↓
4. markdown_copies/ (cleaned text for analysis)
   ↓
5. Research synthesis & findings
```

## Scripting for Bulk Operations

### Convert and Create Summary
```bash
#!/bin/bash
# convert.sh

echo "Converting HTML to Markdown..."
python html-to-markdown-parser/scripts/html_to_markdown.py --batch html_copies markdown_copies

# Count results
echo ""
echo "Conversion complete:"
find markdown_copies -name "*.md" | wc -l
echo "Markdown files created"

# List by outlet
echo ""
echo "Files by outlet:"
for dir in markdown_copies/*/; do
  count=$(find "$dir" -name "*.md" | wc -l)
  outlet=$(basename "$dir")
  echo "  $outlet: $count files"
done
```

## Troubleshooting & Tips

### Tip: Verify Installation
```bash
python -c "import trafilatura; import bs4; print('Dependencies OK')"
```

### Tip: Check Conversion Rate
```bash
# Count HTML files
find html_copies -name "*.html" | wc -l

# Count Markdown files after conversion
find markdown_copies -name "*.md" | wc -l
```

### Issue: Memory on Large Batches
If processing many files causes issues:
1. Convert by outlet: `python scripts/html_to_markdown.py --batch html_copies/bellingcat`
2. Increase available memory or process in smaller batches

### Issue: Encoding Errors
The script handles encoding gracefully with error='replace', but if issues occur:
```bash
# Manually check encoding of problematic file
file -i html_copies/outlet/article.html

# Convert specific file with debugging
python -c "
from pathlib import Path
from html_to_markdown import convert_file
convert_file(Path('html_copies/outlet/article.html'))
"
```
