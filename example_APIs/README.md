# Example OpenAPI Specifications

This directory contains real-world OpenAPI/Swagger specifications for testing and development.

## Files

### petstore.json
- **Source:** https://petstore.swagger.io/v2/swagger.json
- **Size:** 14KB
- **Use Case:** Simple example API, great for testing basic CLI generation
- **Endpoints:** ~20 endpoints for a pet store domain

### github-api.json
- **Source:** https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.json
- **Size:** 12MB
- **Use Case:** Production-grade, complex API with real-world patterns
- **Endpoints:** 1000+ endpoints covering all GitHub REST functionality
- **Features:** Authentication, pagination, rate limits, nested resources

### stripe-api.json
- **Source:** https://github.com/stripe/openapi/raw/main/spec3.json
- **Size:** 291KB
- **Use Case:** Payment API with comprehensive financial domain modeling
- **Endpoints:** 500+ endpoints for payments, charges, customers, etc.
- **Features:** Complex request/response models, extensive error handling

## Usage

Use these specs to:
- Test OpenAPI parsing and validation
- Generate sample CLI commands and help text
- Test CLI generation with different API complexities
- Validate parameter mapping and endpoint discovery

## Updating Specs

To refresh these specs with latest versions:

```bash
cd example_APIs
curl -s https://petstore.swagger.io/v2/swagger.json -o petstore.json
curl -s https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.json -o github-api.json
curl -s https://github.com/stripe/openapi/raw/main/spec3.json -o stripe-api.json
```
