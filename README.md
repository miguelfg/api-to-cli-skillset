# Product Requirements Document: API-to-CLI Skillset

## 1. Vision & Goal

**One-sentence goal:** Transform API documentation into production-ready Python Click CLI tools, enabling developers to quickly build and test API integrations without manual client/CLI boilerplate.

**MVP Output:** Given an API specification (OpenAPI, GraphQL, AsyncAPI, etc.) → generate `client.py`, `cli.py`, and `README.md`

---

## 2. Target Users & Use Cases

**Primary Users:**
- API consumers building integrations
- DevRel / API evangelists
- QA engineers automating API testing
- Data engineers querying APIs

**Top 3 Use Cases:**
1. **Rapid API Exploration** — Developers receive a new API spec → within 2 minutes, they have a working CLI to test endpoints
2. **Test Automation** — QA engineers generate a CLI from OpenAPI/GraphQL specs → immediately start writing smoke tests without SDK setup
3. **Integration Scaffolding** — Data engineers turn Stripe, GitHub, Twilio specs into ready-to-run Python clients with auth baked in

---

## 3. Core Features (v1)

### 3.1 Input Support
- ✅ OpenAPI 3.x (URL or file)
- ✅ OpenAPI 3.0 YAML/JSON
- 🚀 GraphQL SDL (introspection or `.graphql` file)
- 🚀 AsyncAPI (v2.x, Kafka/MQTT/WebSocket patterns)
- ⚠️ LLM-assisted parsing for HTML/Markdown docs (future)

### 3.2 Generated Artifacts
- **`client.py`** — Type-hinted HTTP client (httpx async-capable)
  - Pydantic models for request/response validation
  - Auto-discovery of auth (API key, Bearer, OAuth2, custom headers)
  - Built-in retry + rate-limit awareness
- **`cli.py`** — Click CLI with one command per endpoint
  - Help text auto-populated from OpenAPI descriptions
  - Argument validation from schema
  - Output formatting (JSON, table, raw)
- **`README.md`** — Quick-start guide
  - Installation instructions
  - Auth setup (env vars, `.env` template, OS keychain options)
  - Example commands + expected output
  - Links to original API docs

### 3.3 Authentication Support
- API Key (header/query)
- Bearer tokens (JWT, custom)
- Basic auth
- OAuth2 client credentials (store refresh tokens)
- Custom headers
- Credential storage: env vars, `.env`, OS keychain (`~/.config/apicli/config.toml`)

### 3.4 API Coverage Rules
- Generate all endpoints (option to filter by tags/path prefix/operation ID)
- Pagination: auto-detect common patterns (limit/offset, cursor, `_next`)
- Retry strategy: exponential backoff for 5xx, configurable
- Rate limiting: detect `X-RateLimit-*` headers, implement token bucket

---

## 4. CLI Behavior (User Contract)

```bash
# Primary command
apicli generate --spec <url|file.json|file.yaml> --out ./my_api_client

# Output structure
./my_api_client/
  ├── client.py              # HTTP client + Pydantic models
  ├── cli.py                 # Click CLI entry point
  ├── README.md              # Quick-start docs
  ├── .env.example           # Template for credentials
  └── pyproject.toml         # Dependencies (httpx, pydantic, click)

# Using the generated CLI
cd my_api_client
pip install -e .
export API_KEY="sk_live_..."

my_api_client get /users --limit 10
my_api_client create /users --name "Alice" --email "alice@example.com"
```

---

## 5. Technical Architecture

- **Framework:** Click for CLI, httpx for async HTTP
- **Typing:** Pydantic v2 for models, Python 3.9+ compatible
- **Code Gen:** Jinja2 templates for client/CLI scaffolding
- **Parsing:**
  - OpenAPI: `pydantic-openapi-schema` or custom parser
  - GraphQL: `graphql-core` introspection
  - AsyncAPI: `asyncapi` parser
- **Testing:** golden-file tests on generated code; integration tests with real APIs (Petstore, Stripe sandbox)

---

## 6. Success Metrics (v1 Done When…)

1. ✅ OpenAPI 3.x → fully functional `client.py` + `cli.py` (100% endpoint coverage)
2. ✅ Auth (API key, Bearer, Basic) → credentials securely resolved from env/keychain
3. ✅ Generated CLI passes smoke tests on Stripe, GitHub, Twilio sample specs
4. ✅ README is clear enough for a new dev to `pip install` and run first command in <2 min
5. ✅ Typed models prevent common request mistakes (missing required params, type mismatches)
6. ✅ Code generation is deterministic (same spec → same output)
7. ✅ Package ships on PyPI; installable via `pip install apicli`

---

## 7. Out of Scope (v1)

- WebSocket subscriptions (AsyncAPI future phase)
- Custom business logic inference
- UI/dashboard generation
- Multiple language support (Python first)
- Rate-limit enforcement (detection only)
- GraphQL mutations with complex input types (v2)
- SOAP/WSDL support (v2)

---

## 8. AI Agent Skillset Integration

**Skill Definition:** One skill per API standard

```
Skills:
- openapi_to_cli    → OpenAPI 3.x URL/file → CLI project
- graphql_to_cli    → GraphQL endpoint/SDL → CLI project
- asyncapi_to_cli   → AsyncAPI YAML/JSON → event subscriber CLI
```

**Interface (standardized):**
```python
async def run(input: SpecArtifact) -> GeneratedProject:
    # Parse spec, validate, generate client + CLI
    # Return Project(client_py, cli_py, readme_md, env_example)
```

---

## 9. Reference APIs for Testing

Gold-standard OpenAPI specs:
- **Stripe** (https://github.com/stripe/openapi) — payment patterns
- **GitHub REST** (raw.githubusercontent.com/github/rest-api-description) — large, complex auth
- **Twilio** (github.com/twilio/twilio-oai) — real-world enterprise API
- **Slack Web API** (github.com/slackapi/slack-api-specs) — REST + events
- **Petstore** (petstore.swagger.io) — demo/baseline

---

## 10. Development Roadmap

**Phase 1 (v0.1-v1.0):** OpenAPI 3.x core
**Phase 2 (v1.1-v2.0):** GraphQL + AsyncAPI
**Phase 3 (v2.1+):** gRPC, RAML, enhanced LLM parsing, UI gen
