#!/usr/bin/env python3
"""
Convert HTML articles to clean, readable Markdown with metadata extraction.
Intelligently extracts main article content while removing navigation, ads, and clutter.
"""

import os
import sys
import json
from pathlib import Path
from typing import Optional, Dict, Tuple
import re
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

try:
    from bs4 import BeautifulSoup
    HAS_BEAUTIFULSOUP = True
except ImportError:
    HAS_BEAUTIFULSOUP = False

try:
    import trafilatura
    HAS_TRAFILATURA = True
except ImportError:
    HAS_TRAFILATURA = False


class HTMLToMarkdownConverter:
    """Convert HTML to clean Markdown with smart article extraction."""

    def __init__(self, html_content: str, source_url: str = ""):
        self.html_content = html_content
        self.source_url = source_url
        self.soup = None
        self.metadata = {}

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special HTML entities
        text = text.replace('\xa0', ' ')
        return text.strip()

    def _extract_metadata(self) -> Dict[str, str]:
        """Extract title, author, date from HTML metadata."""
        metadata = {
            'title': '',
            'author': '',
            'date': '',
            'source_url': self.source_url
        }

        if not self.soup:
            return metadata

        # Try to extract title
        title_elem = self.soup.find('h1') or self.soup.find('title')
        if title_elem:
            metadata['title'] = self._clean_text(title_elem.get_text())
        else:
            metadata['title'] = self.source_url.split('/')[-1]

        # Try common metadata patterns for author
        for meta_tag in self.soup.find_all('meta'):
            content = meta_tag.get('content', '')
            name = meta_tag.get('name', '').lower()
            property_attr = meta_tag.get('property', '').lower()

            if 'author' in name or 'author' in property_attr:
                metadata['author'] = self._clean_text(content)
            elif 'article:published_time' in property_attr or 'publish' in name:
                metadata['date'] = self._clean_text(content)
            elif 'date' in name:
                metadata['date'] = self._clean_text(content)

        # Fallback: look for common author/date patterns in text
        if not metadata['author']:
            author_elem = self.soup.find(['span', 'div'], class_=re.compile(r'author|byline', re.I))
            if author_elem:
                metadata['author'] = self._clean_text(author_elem.get_text())

        return metadata

    def _extract_article_content(self) -> Optional[str]:
        """Extract main article content using best available method."""
        if HAS_TRAFILATURA:
            # Trafilatura is best for news extraction
            extracted = trafilatura.extract(self.html_content, include_comments=False)
            if extracted:
                return extracted

        if HAS_BEAUTIFULSOUP:
            return self._extract_with_beautifulsoup()

        # Fallback: simple extraction
        return self._simple_extract()

    def _extract_with_beautifulsoup(self) -> str:
        """Use BeautifulSoup to extract article content intelligently."""
        # Create a fresh soup copy for extraction to avoid state issues
        soup = BeautifulSoup(str(self.soup), 'html.parser')

        # Remove common non-content elements
        for element in soup.find_all(['script', 'style', 'nav', 'footer', 'aside']):
            element.decompose()

        # Remove elements with common ad/tracking classes
        ad_patterns = ['ad', 'advertisement', 'sidebar', 'related', 'comment', 'footer', 'nav', 'social']
        for element in soup.find_all(True):
            try:
                classes = ' '.join(element.get('class', []) or [])
                if any(pattern in classes.lower() for pattern in ad_patterns):
                    if element.name not in ['article', 'main']:
                        element.decompose()
            except:
                pass  # Skip if element was already decomposed

        # Try to find main article container
        article = (soup.find(['article', 'main']) or
                   soup.find('div', class_=re.compile(r'content|article|post', re.I)))

        if article:
            content = article.get_text(separator='\n', strip=True)
        else:
            # Fallback to body
            body = soup.find('body') or soup
            content = body.get_text(separator='\n', strip=True)

        return content

    def _simple_extract(self) -> str:
        """Simple text extraction fallback."""
        # Remove script and style tags
        for tag in self.html_content.find_all(['script', 'style']):
            tag.decompose()
        return self.html_content.get_text(separator='\n', strip=True)

    def to_markdown(self) -> str:
        """Convert HTML to Markdown format."""
        # Parse HTML
        try:
            self.soup = BeautifulSoup(self.html_content, 'html.parser')
        except Exception as e:
            print(f"Warning: Failed to parse HTML: {e}", file=sys.stderr)
            return ""

        # Extract metadata
        self.metadata = self._extract_metadata()

        # Extract article content
        content = self._extract_article_content() or ""

        # Build Markdown
        markdown = []

        # Add metadata header
        if self.metadata['title']:
            markdown.append(f"# {self.metadata['title']}\n")

        metadata_items = []
        if self.metadata.get('author'):
            metadata_items.append(f"**Author:** {self.metadata['author']}")
        if self.metadata.get('date'):
            metadata_items.append(f"**Date:** {self.metadata['date']}")
        if self.metadata.get('source_url'):
            parsed_url = urlparse(self.metadata['source_url'])
            domain = parsed_url.netloc
            metadata_items.append(f"**Source:** [{domain}]({self.metadata['source_url']})")

        if metadata_items:
            markdown.append("\n".join(metadata_items))
            markdown.append("\n---\n")

        # Add content
        if content:
            markdown.append(self._clean_text(content))

        return "\n".join(markdown)

    def get_metadata(self) -> Dict[str, str]:
        """Get extracted metadata."""
        if not self.metadata:
            self._extract_metadata()
        return self.metadata


def convert_file(html_file: Path, output_dir: Optional[Path] = None) -> Path:
    """
    Convert a single HTML file to Markdown.

    Args:
        html_file: Path to HTML file
        output_dir: Directory to save markdown file (default: same as HTML file)

    Returns:
        Path to created markdown file
    """
    if not html_file.exists():
        raise FileNotFoundError(f"HTML file not found: {html_file}")

    with open(html_file, 'r', encoding='utf-8', errors='replace') as f:
        html_content = f.read()

    converter = HTMLToMarkdownConverter(html_content, str(html_file))
    markdown = converter.to_markdown()

    # Determine output path
    if output_dir is None:
        output_dir = html_file.parent

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{html_file.stem}.md"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown)

    return output_file


def batch_convert(input_dir: Path, output_dir: Optional[Path] = None) -> Dict[str, Path]:
    """
    Convert all HTML files in a directory to Markdown.

    Args:
        input_dir: Directory containing HTML files
        output_dir: Directory to save markdown files (default: input_dir/markdown)

    Returns:
        Dictionary mapping source HTML files to generated Markdown files
    """
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    if output_dir is None:
        output_dir = input_dir / "markdown"

    output_dir.mkdir(parents=True, exist_ok=True)
    results = {}

    html_files = list(input_dir.glob("**/*.html"))
    if not html_files:
        print(f"No HTML files found in {input_dir}")
        return results

    print(f"Converting {len(html_files)} HTML files...\n")

    for i, html_file in enumerate(html_files, 1):
        try:
            md_file = convert_file(html_file, output_dir)
            results[str(html_file)] = str(md_file)
            print(f"[{i}/{len(html_files)}] ✓ {html_file.name} → {md_file.name}")
        except Exception as e:
            print(f"[{i}/{len(html_files)}] ✗ {html_file.name} - {str(e)}")

    print(f"\n✓ Conversion complete! {len(results)}/{len(html_files)} files converted")
    print(f"Markdown files saved to: {output_dir}")

    return results


def main():
    """Command-line interface."""
    if len(sys.argv) < 2:
        print("""
Usage:
  # Convert single file
  python html_to_markdown.py <html_file> [output_dir]

  # Convert directory
  python html_to_markdown.py --batch <input_dir> [output_dir]

Examples:
  python html_to_markdown.py article.html
  python html_to_markdown.py --batch ./html_copies ./markdown_output
        """)
        sys.exit(1)

    if sys.argv[1] == "--batch":
        input_dir = Path(sys.argv[2])
        output_dir = Path(sys.argv[3]) if len(sys.argv) > 3 else None
        batch_convert(input_dir, output_dir)
    else:
        html_file = Path(sys.argv[1])
        output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else None
        md_file = convert_file(html_file, output_dir)
        print(f"✓ Converted: {md_file}")


if __name__ == "__main__":
    main()
