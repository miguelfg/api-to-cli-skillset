# doc-to-prd Skill Updates

## Summary

The `doc-to-prd` skill has been enhanced with comprehensive documentation templates, Makefile/uvicorn integration guidance, and project management best practices.

## What's New

### 1. Comprehensive PRD Template

**File:** `references/PRD_template.md`

A complete template for generating Product Requirements Documents with:

#### Core Sections
- **Introduction** - Overview, purpose, target audience, key features
- **Installation** - System requirements, installation methods, dependencies
- **Configuration** - Environment variables, config files, management commands
- **Authentication** - API key setup, methods, error handling, best practices

#### Technical Documentation
- **Endpoint Reference** - Complete API documentation with examples for each resource
- **Input/Output Examples** - Single requests, batch processing, multiple formats
- **Caching** - Configuration, management, strategy, best practices
- **Rate Limiting** - API limits, client-side handling, configuration
- **Error Handling** - Error classification, response format, common issues
- **Logging** - Log levels, configuration, format, verbose mode

#### Development & Project Management
- **Best Click Practices** - CLI design, standard options, error messages, performance
- **Makefile & Project Management** - Project structure, Makefile commands, uvicorn integration

### 2. Makefile Template

**File:** `templates/Makefile_sample`

Sample Makefile with colorized output and organized targets:

**Installation Targets:**
```bash
make install          # Development mode
make install-dev      # With dev dependencies
```

**Code Quality Targets:**
```bash
make lint             # Run linters
make format           # Format code
make format-check     # Check format
```

**Testing Targets:**
```bash
make test             # Tests with coverage
make test-fast        # Fast tests
make test-verbose     # Verbose output
make test-watch       # Watch mode
```

**Development Targets:**
```bash
make dev              # Verify CLI
make serve            # Dev server (uvicorn)
make serve-prod       # Production server
```

**Documentation & Build:**
```bash
make docs             # Generate docs
make prd              # Show PRD location
make build            # Build packages
make clean            # Clean artifacts
make release          # Prepare release
```

**Utility Targets:**
```bash
make info             # Project info
make status           # Git & deps status
make help             # Show all commands
```

### 3. Uvicorn Integration Guide

**File:** `references/uvicorn_guide.md`

Comprehensive guide for using uvicorn with Python CLI projects:

#### Topics Covered
- When to use uvicorn (and when not to)
- Installation and setup
- Basic usage and hello world
- Configuration (CLI options, config file, YAML)
- Integration with Click CLI projects
- Mock API server example
- Makefile integration
- Advanced usage (middleware, logging, env vars)
- Troubleshooting guide
- Performance tuning
- Deployment considerations
- Monitoring and health checks

#### Example Configurations

**Development:**
```bash
make serve
# Runs with auto-reload
```

**Production:**
```bash
make serve-prod
# Runs with multiple workers
```

**Debug:**
```bash
make serve-debug
# Verbose logging
```

### 4. Updated SKILL.md

The main `SKILL.md` file now includes:

#### New Sections
- **PRD Template Structure** - Overview of template sections
- **Makefile & Project Management** - Details on Makefile targets
- **uvicorn Integration** - How uvicorn fits into the workflow
- **Integration with api-to-cli Workflow** - Complete workflow diagram
- **Usage Tips** - Best practices for using templates
- **References** - Links to all new documentation

#### Key Highlights
- PRD now includes all necessary sections for production-ready CLI clients
- Makefile provides common development tasks with color output
- uvicorn handles optional development server functionality
- All templates are customizable placeholders

## Files Structure

```
skills/doc-to-prd/
├── SKILL.md                          # Updated with new sections
├── DOC_TO_PRD_UPDATE.md             # This file
├── references/
│   ├── PRD_template.md              # NEW: Complete PRD template
│   └── uvicorn_guide.md             # NEW: Uvicorn usage guide
└── templates/
    ├── default_config.json          # Existing
    └── Makefile_sample              # NEW: Sample Makefile
```

## Key Features

### 1. PRD Template (PRD_template.md)

**Placeholders for Easy Customization:**
- `[API Name]` → Your API name
- `[api-prefix]` → Environment variable prefix
- `[cli-name]` → CLI tool name
- `[RESOURCE_NAME]` → API resource names
- `[Limit]` → Rate limit values
- `[org]` → Organization name

**Comprehensive Sections:**
- 12 major sections covering all aspects
- Installation with multiple methods
- Configuration management
- Authentication best practices
- Complete endpoint reference with CRUD examples
- Batch processing examples
- Caching and rate limiting strategies
- Error handling patterns
- Logging configuration
- CLI best practices
- Makefile and uvicorn integration

### 2. Makefile Template (Makefile_sample)

**Features:**
- Colorized output (green for success, yellow for info)
- Self-documenting with `make help`
- 25+ targets organized by category
- Includes uvicorn targets for serving
- Support for virtual environments
- Clean, build, and release targets
- Test coverage and fast test modes
- Development environment setup

**Example Usage:**
```bash
# Show all available commands
make help

# Install and setup
make install-dev
make lint
make format

# Run tests
make test                 # With coverage
make test-fast           # Without coverage
make test-verbose        # Verbose output

# Development server
make serve               # Auto-reload dev server
make serve-prod         # Production server

# Build and release
make build
make release
```

### 3. Uvicorn Integration Guide (uvicorn_guide.md)

**Coverage:**
- When to use uvicorn and when not to
- Installation and setup
- Configuration methods (CLI, .ini, .yaml)
- Integration with Click CLI projects
- Mock API server example
- Makefile integration
- Custom middleware and logging
- Performance tuning
- Deployment patterns
- Troubleshooting guide
- Monitoring and health checks

**Example Configuration:**

```makefile
serve:
	uvicorn src.[cli_name].server:app --reload --port 8000

serve-prod:
	uvicorn src.[cli_name].server:app --host 0.0.0.0 --port 8000 --workers 4
```

## Workflow Integration

```
API Documentation (OpenAPI/HTML)
    ↓
[api-to-doc] → openapi.yaml
    ↓
[doc-to-prd] → PRD.md (using new template)
    ↓
[prd-to-cli] → Python Click CLI Project
    ↓
Use Makefile for development:
  - make install-dev
  - make lint / make format
  - make test
  - make serve (optional uvicorn server)
    ↓
Deploy with make release
```

## Usage Examples

### Generating a PRD

```bash
# Using api-to-doc output
/doc-to-prd @openapi.yaml PRD.md

# The generated PRD.md will include:
# - Installation instructions
# - Configuration examples
# - Endpoint reference with examples
# - Batch processing guide
# - Caching and rate limiting
# - Complete Makefile example
# - uvicorn server setup instructions
```

### Using the Generated Makefile

```bash
# Setup development environment
cd my-api-client
make install-dev

# Check code quality
make lint
make format

# Run tests
make test

# Optional: Run development server
make serve

# Prepare for release
make clean
make build
make release
```

### Using Uvicorn

```bash
# Development with auto-reload
make serve

# Production with workers
make serve-prod

# Test the server
curl http://localhost:8000/health
```

## Template Customization

After generating PRD.md:

1. **Replace Placeholders:**
   - `[API Name]` → Your actual API name
   - `[cli-name]` → Your CLI tool name
   - `[api-prefix]` → Your env var prefix

2. **Update Rate Limits:**
   - Replace `[Limit]` with actual values

3. **Customize Examples:**
   - Update endpoint examples with real data
   - Adjust parameter names to match your API

4. **Tailor Makefile:**
   - Adjust Python version if needed
   - Add project-specific targets

## Best Practices

### PRD.md
✓ Review template thoroughly
✓ Keep examples up-to-date
✓ Test all documented endpoints
✓ Version control the PRD.md
✓ Update when API changes

### Makefile
✓ Use for all development tasks
✓ Keep targets simple and focused
✓ Add project-specific targets
✓ Document custom targets
✓ Use standard target names

### Uvicorn
✓ Use for development/testing only
✓ Use proper reverse proxy for production
✓ Monitor health endpoints
✓ Enable logging appropriately
✓ Use environment-specific configs

## Reference Links

- **[PRD_template.md](references/PRD_template.md)** - Full PRD template
- **[uvicorn_guide.md](references/uvicorn_guide.md)** - Uvicorn usage guide
- **[Makefile_sample](templates/Makefile_sample)** - Sample Makefile
- **[SKILL.md](SKILL.md)** - Main skill documentation

## What's Next

Possible future enhancements:

- [ ] Auto-populate placeholders from user input
- [ ] Generate project structure alongside PRD
- [ ] Docker configuration template
- [ ] GitHub Actions CI/CD template
- [ ] Pre-commit hooks setup
- [ ] Environment-specific Makefile variants
- [ ] Automated changelog generation

## Support

For issues or questions:

1. Review the PRD template sections
2. Check the Makefile examples
3. Consult the uvicorn guide
4. Review skill documentation

---

**Version:** 1.0
**Last Updated:** 2024-01-15
