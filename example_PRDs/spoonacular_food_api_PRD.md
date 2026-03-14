# Spoonacular Food API Python Client - Product Requirements Document

**API Version:** 1.0.0
**Base URL:** `https://api.spoonacular.com`
**Resources:** `recipes, ingredients, products, menuitems, mealplanner`

## Introduction

### Overview

This document defines the requirements for a Python Click CLI client for the Spoonacular Food API. The initial scope covers a representative subset of the official API documentation centered on recipe search, recipe lookup, ingredient search, grocery product search, menu item search, and meal-plan generation.

### Purpose

- Provide a practical CLI for common Spoonacular discovery workflows.
- Support recipe, ingredient, product, menu item, and meal-planning queries from the command line.
- Preserve the API's authentication, pagination, and quota behavior in a developer-friendly interface.

## Implementation Decisions

- CLI Name: `spoonacular-cli`
- Python Version: `>=3.10`
- HTTP Library: `requests`
- Authentication: `apiKey` query parameter or `x-api-key` header, derived from official docs
- Credentials Configuration: `env_vars`
- Timeout: `30s total timeout`
- Retry Policy: `3 attempts`, `1s base`, `x2 backoff`, retry on `408,429,500,502,503,504`
- Output Formats: `json,csv,xlsx,sqlite`
- Output Accepted Formats and Default: `default_xlsx__accepted_xlsx_csv_sqlite`
- Batch Input Formats: `csv|txt|both`
- Default Save Data Mode: `timestamped`
- Lint/Format Toolchain: `ruff check --fix` + `ruff format`

## Installation

### System Requirements

- Python 3.10+
- `uv`

### Installation

```bash
git clone <generated-project-repo>
cd spoonacular-cli
uv sync
```

### Verify Installation

```bash
uv run spoonacular-cli --help
```

### Validation Requirements

The generated CLI project must include live smoke validation for read-oriented commands during the `prd-to-cli` step.

Required validation behavior:
- Run low-volume GET/list validation against each generated read/list command or GET endpoint mapping.
- Prefer list/read commands that do not require fabricated identifiers.
- Limit returned records to a small number such as `10` whenever the API supports pagination or `number` style parameters.
- Use the API's documented parameter names instead of inventing replacements.
- Treat these live validations as required acceptance checks.

## Configuration

### Environment Variables

The CLI should support environment-variable based configuration as the default credential mode.

```bash
SPOONACULAR_API_KEY=your_api_key_here
SPOONACULAR_BASE_URL=https://api.spoonacular.com
SPOONACULAR_TIMEOUT=30
SPOONACULAR_VERBOSE=false
```

### Configuration Priority

1. CLI flags
2. Environment variables
3. Config file values when explicitly enabled
4. Built-in defaults

## Authentication

The Spoonacular API requires an API key for every request.

- Query parameter mode: `?apiKey=YOUR_API_KEY`
- Header mode: `x-api-key: YOUR_API_KEY`

The generated client should prefer `x-api-key` header injection when possible and allow query-parameter fallback for compatibility with documented examples.

## Endpoint Reference

### RECIPES Resource

#### 1. Search Recipes

- `/recipes/complexSearch` — Search recipes with natural-language query, dietary filters, cuisines, pagination, and sorting.

Key parameters:
- `query`
- `diet`
- `cuisine`
- `number`
- `offset`

#### 2. Get Recipe Information

- `/recipes/{id}/information` — Retrieve detailed recipe information by recipe id.

Key parameters:
- `id`
- `includeNutrition`
- `addWinePairing`
- `addTasteData`

### INGREDIENTS Resource

#### 1. Search Ingredients

- `/food/ingredients/search` — Search whole-food ingredients by name with optional nutrition-oriented filters.

Key parameters:
- `query`
- `addChildren`
- `metaInformation`
- `number`
- `offset`

### PRODUCTS Resource

#### 1. Search Grocery Products

- `/food/products/search` — Search packaged grocery products such as yogurt or frozen pizza.

Key parameters:
- `query`
- `addProductInformation`
- `number`
- `offset`

### MENUITEMS Resource

#### 1. Search Menu Items

- `/food/menuItems/search` — Search fast-food and chain-restaurant menu items.

Key parameters:
- `query`
- `addMenuItemInformation`
- `number`
- `offset`

### MEALPLANNER Resource

#### 1. Generate Meal Plan

- `/mealplanner/generate` — Generate a daily or weekly meal plan.

Key parameters:
- `timeFrame`
- `targetCalories`
- `diet`
- `exclude`

## Input/Output Examples

### Example CLI Calls

```bash
uv run spoonacular-cli recipes list --query pasta --number 10
uv run spoonacular-cli recipes get 716429
uv run spoonacular-cli ingredients list --query banana --number 10
uv run spoonacular-cli products list --query pizza --number 10
uv run spoonacular-cli menuitems list --query burger --number 10
uv run spoonacular-cli mealplanner list --timeFrame day --targetCalories 2000
```

### Example Batch CSV

```csv
method,endpoint,query,number
GET,/recipes/complexSearch,pasta,10
GET,/food/ingredients/search,banana,10
GET,/food/products/search,pizza,10
```

### Example Batch JSONL

```json
{"method":"GET","endpoint":"/recipes/complexSearch","query":"pasta","number":10}
{"method":"GET","endpoint":"/mealplanner/generate","timeFrame":"day","targetCalories":2000}
```

## Rate Limiting

The API uses plan-based quotas and request-rate limits.

- Requests typically cost `1 point`, with some endpoints adding per-result or optional-feature costs.
- Free-tier rate limit documented in the guide: `60 requests in 1 minute`.
- Exceeding daily quota can return HTTP `402`.
- Exceeding per-second or per-minute limits can return HTTP `429`.

The client should:
- surface quota and throttling errors clearly
- retry only on transient retryable responses
- avoid aggressive concurrency by default

## Error Handling

Handle these categories explicitly:

- `401`/auth-related failures caused by missing or invalid API key
- `402` quota exhaustion
- `404` invalid path or entity id
- `429` rate limit exceeded
- `5xx` transient upstream failures

## Logging

The CLI should log concise request context in normal mode and richer request/response debugging in verbose mode.

Recommended log fields:
- resource
- endpoint path
- HTTP method
- request duration
- response status
- retry count

## Makefile & Project Management

The generated project should include at least:

- `make install`
- `make help`
- `make test`
- example resource list targets where practical

## Notes for Generation

- The upstream docs use mixed resource paths under `/recipes`, `/food/...`, and `/mealplanner`.
- During `prd-to-cli`, generated resource command paths may need follow-up edits so each resource command maps to its documented endpoint rather than a guessed fallback path.
- Preserve the exact Spoonacular parameter names such as `number`, `offset`, `includeNutrition`, `addProductInformation`, and `timeFrame`.
