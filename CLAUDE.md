# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**API-to-CLI Skillset** is a Claude Code skillset project that provides two complementary skills for converting API documentation into Python Click CLI projects:

1. **`doc-to-prd`** — Generates a comprehensive PRD.md from an OpenAPI specification (JSON/YAML file or URL)
2. **`prd-to-cli`** — Generates a full production-ready Python Click CLI project from a PRD.md file

**Goal:** Enable developers to quickly build and test API integrations without manual client/CLI boilerplate.

## Skill Architecture

### Two-Step Workflow

```
OpenAPI Spec (JSON/YAML)
    ↓
[doc-to-prd skill]
    ↓
PRD.md (comprehensive API documentation with code examples)
    ↓
[prd-to-cli skill]
    ↓
Python Click CLI Project (full project structure with batch processing)
```

### Skill Components

**`skills/doc-to-prd/`**
- **Purpose:** Parse OpenAPI specs and generate detailed PRD.md
- **Input:** OpenAPI/Swagger JSON/YAML file or URL
- **Output:** PRD.md with installation, authentication, endpoint reference, code examples, best practices
- **Key Script:** `scripts/generate_prd.py` — Main parser and generator
- **References:** `references/openapi_mapping.md`, `references/prd_template.md`

**`skills/prd-to-cli/`**
- **Purpose:** Parse PRD.md and generate a full Click CLI project
- **Input:** PRD.md file
- **User Configuration:** Batch formats, output formats, timestamp patterns (via `askUserQuestion`)
- **Output:** Full project structure with CLI, client library, batch processor, configuration
- **Key Script:** `scripts/generate_cli_from_prd.py` — Main project generator
- **References:** `references/input_format_specs.md`, `references/output_configuration.md`, `references/generated_structure.md`

## Common Development Tasks

### Creating/Testing a Skill

1. **Understand requirement** — Clarify with user what the skill should do
2. **Create skill structure** — Use skill-creator skill's `init_skill.py` to scaffold
3. **Implement generation logic** — Write main script in `scripts/`
4. **Create references** — Document usage patterns in `references/`
5. **Update SKILL.md** — Write metadata and instructions
6. **Package** — Use skill-creator's `package_skill.py` to validate and create `.skill` file
7. **Unpackage** — Unzip `.skill` file into `skills/` folder for local use

### Working with Existing Skills

**To modify a skill:**
1. Edit files directly in `skills/{skill-name}/`
2. Update `SKILL.md` (frontmatter: name/description; body: instructions)
3. Update scripts in `scripts/` and references in `references/`
4. Test by invoking the skill with test inputs

**To test user questions in a skill:**
- Use `askUserQuestion` tool to define configuration preferences
- Questions guide the generation process (formats, paths, timestamps, etc.)
- Review `references/` files to understand expected inputs and outputs

### Example Skill Invocation

```bash
# Skill 1: Generate PRD from OpenAPI
/doc-to-prd @example_APIs/petstore.json

# Skill 2: Generate Click CLI from PRD
/prd-to-cli @example_PRDs/PRD.md
# User answers questions about batch formats, output options, timestamp format
# → Generates full project in output directory
```

## Using askUserQuestion for Fast-Paced Narrowing

When implementing skills that need to handle vague or open-ended user requests, use `askUserQuestion` with focused, fast-paced questions to narrow requests into specific, actionable tasks.

### Pattern: Question Cascade

**1. Maximum 4 questions per round** — Keep interactions snappy; avoid overwhelming users with too many choices at once.

**2. Question prioritization** — Ask the most critical decision first:
   - What is the scope? (this determines everything else)
   - What format/output? (enables specific generation)
   - How to handle edge cases? (configuration details)

**3. Build on answers** — Each answer informs the next question. Use context from prior answers to make subsequent questions more relevant.

**Example from `prd-to-cli`:**

```
Question 1: Batch input formats?  (narrows to CSV, TXT, or both)
  ↓ User answers: "CSV and TXT"
Question 2: Project details?  (name, output path)
  ↓ User answers: "my_client, ./projects"
Question 3: Output formats?  (JSON, CSV, XLSX selection)
  ↓ User answers: "JSON and XLSX"
Question 4: Timestamp configuration?  (include? format?)
  ↓ User answers: "Yes, YYYYMMDD_HHMMSS"
  → Generate with all preferences configured
```

### Best Practices

**Do:**
- Ask one decision per question (mutually exclusive options)
- Provide 2-4 options per question
- Use clear, specific language: "Batch input formats?" vs vague "What do you want?"
- Include descriptions for each option to aid understanding
- Start broad, narrow down with follow-ups

**Don't:**
- Ask 5+ questions in one round (user context exhaustion)
- Mix multiple decisions in one question ("formats AND destination?")
- Assume prior context from previous skill invocations (each session is fresh)
- Leave questions open-ended ("How should we configure this?")

### Implementation Example

```python
from src.batch_processor import BatchProcessor
from src.config import Config

# Ask questions to gather configuration
questions = [
    {
        "question": "Which batch input formats to accept?",
        "header": "Input Formats",
        "options": [
            {"label": "CSV only", "description": "Comma-separated values"},
            {"label": "TXT (JSON Lines) only", "description": "One JSON object per line"},
            {"label": "Both CSV and TXT", "description": "Maximum flexibility"}
        ]
    },
    {
        "question": "Output format preferences?",
        "header": "Output Formats",
        "multiSelect": True,
        "options": [
            {"label": "JSON", "description": "Structured data (default)"},
            {"label": "CSV", "description": "Tabular format"},
            {"label": "XLSX", "description": "Excel workbook"}
        ]
    }
]

# User answers flow into generation logic
# → Generates configuration automatically
```

## Key Development Patterns

### PRD.md Structure

Expectations for PRD.md files (output of skill 1, input to skill 2):

- **Headers:** `# PRD Title`, `**Version:**`, `**Base URL:**`
- **Resource Sections:** `### RESOURCE_NAME` (e.g., `### PETS`, `### ORDERS`)
- **Endpoint Subsections:** `#### 1. Endpoint Description`
- **Code Examples:** Python `requests` library examples for each endpoint
- **Configuration:** `.env` setup, auth methods, output formats

**Example location:** `example_PRDs/PRD.md`

### Generated Project Structure (from skill 2)

```
project_name/
├── src/
│   ├── cli.py                    # Click CLI entry point with global options
│   ├── client.py                 # HTTP client wrapper (requests/httpx)
│   ├── config.py                 # Configuration management (.env parsing)
│   ├── batch_processor.py         # Batch request processor (CSV/TXT)
│   └── commands/
│       ├── __init__.py
│       └── {resource}_commands.py # One file per API resource
├── data/                         # User batch input files
├── output/                       # Batch processing results
├── .env.example                  # Configuration template
└── requirements.txt              # Dependencies
```

**Key design:** One Click subcommand group per API resource (extracted from PRD section headers)

### User Preferences for Generation (via askUserQuestion)

When generating a CLI project, the skill asks:

1. **Batch Input Formats** — CSV, TXT (JSON Lines), or both
2. **Project Details** — Project name, output directory
3. **Output Formats** — JSON, CSV, XLSX (single or multiple)
4. **Timestamp Configuration** — Include timestamp in filenames? Format pattern?

These preferences configure `.env` and batch processor behavior.

### Input Format Specifications

**CSV Format (batch requests):**
```
method,endpoint,param1,param2
GET,/pet/findByStatus,available
POST,/pet,Fluffy,available
```

**TXT Format (JSON Lines):**
```json
{"method": "GET", "endpoint": "/pet/1"}
{"method": "POST", "endpoint": "/pet", "name": "Fluffy"}
```

See `skills/prd-to-cli/references/input_format_specs.md` for complete specs.

## Example APIs for Testing

Located in `example_APIs/`:
- `petstore.json` — Simple Swagger 2.0 spec (good for testing)
- `github-api.json` — Complex GitHub REST API
- `stripe-api.json` — Enterprise-grade Stripe API
- `official-spotify-open-api.yml` — OpenAPI 3.0 YAML example

Use these to test skill 1 (API → PRD) and validate generated outputs.

## Notes for Future Development

**From prompts.md (pending enhancements):**
- Consider async Python library (`httpx`) instead of `requests` in generated clients
- Add Makefile to generated projects for common tasks (test, lint, run endpoints)
- Consider `uvicorn` or another tool for CLI project management

**Skill Iteration Pattern:**
When users request improvements after using a skill:
1. Use the skill on real tasks
2. Notice inefficiencies or missing features
3. Update `SKILL.md`, scripts, or references
4. Test with concrete examples
5. Re-package and distribute

## Key Files to Know

- **README.md** — Vision, goals, use cases, success metrics
- **skills/{skill-name}/SKILL.md** — Skill metadata and instructions
- **skills/{skill-name}/scripts/generate_*.py** — Core generation logic
- **skills/{skill-name}/references/*.md** — User documentation and specifications
- **example_APIs/** — Test cases for skill validation
- **example_PRDs/PRD.md** — Example generated PRD output
- **docs/** — API standards comparison and analysis
