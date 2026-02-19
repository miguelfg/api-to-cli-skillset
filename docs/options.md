# API Options for Full Workflow Testing

Use these APIs to test the end-to-end flow:
`api-to-doc` -> `doc-to-prd` -> `prd-to-cli`.

## Option 1: Open-Meteo (Recommended)
- URL: `https://open-meteo.com/`
- Why use it:
  - Free public API
  - No authentication required for core endpoints
  - Good query-parameter coverage for CLI option generation
- Best for:
  - Fast first full-workflow validation

## Option 2: REST Countries
- URL: `https://restcountries.com/`
- Why use it:
  - No authentication
  - Simple and predictable response structures
  - Easy baseline for generated command behavior
- Best for:
  - Smoke tests and parser sanity checks

## Option 3: CoinGecko
- URL: `https://www.coingecko.com/en/api/documentation`
- Why use it:
  - Richer data models and nested payloads
  - Useful to stress output formatting and batch patterns
- Best for:
  - More realistic CLI generation tests after baseline pass

## Suggested Order
1. Open-Meteo
2. REST Countries
3. CoinGecko

