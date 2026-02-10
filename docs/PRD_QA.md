1) Product goal & scope

What’s the one-sentence goal of the project?

What’s the MVP output? (e.g., “Given OpenAPI URL → generates client.py + cli.py + README”)

Which inputs are in-scope for v1?

OpenAPI 3.x URL?

OpenAPI file (yaml/json)?

Postman collection?

HTML docs page (scrape)?

“Anything” with LLM parsing?

Which inputs are explicitly out-of-scope for v1?

2) Target users & use cases

Who is the primary user?

API consumers? Data engineers? DevRel? QA? Freelancers?

Top 3 use cases you want them to accomplish (realistic examples)?

What is the “aha moment” in under 2 minutes after install?

3) CLI behavior (the user-facing contract)

What should the CLI be called? (project name + command name)

What is the primary command flow?

Example: apicli generate --spec <url_or_file> --out ./myclient

What commands do you want in v1?

generate, auth, call, list-endpoints, validate, doctor, etc.?

Do you want the generated CLI to have one command per endpoint, or a generic call command?

4) Generated client architecture

Should the generated client use:

requests or httpx (sync/async)?

Should it generate:

Typed models (Pydantic / dataclasses) or keep it untyped JSON?

Output structure preference:

Single file (client.py) vs package (myclient/…)?

Python version support? (3.9+? 3.10+?)

5) Authentication support

Which auth types must v1 support?

API key header/query, Bearer token, OAuth2 client creds, Basic, custom headers?

How should credentials be stored?

Env vars only? .env? OS keychain? ~/.config/<tool>/config.toml?

Should generated CLI include an auth login helper, or just document env vars?

6) API coverage rules

For OpenAPI: do we generate all endpoints or allow filters?

tags, path prefix, operationId list, include/exclude regex?

How should pagination be handled?

none, “best effort” patterns, or config per API?

Retry / backoff / rate limit handling expectations?

7) Documentation output

What docs must be generated?

README for the generated client, usage examples, .env template, command help text?

Should it generate runnable examples / “smoke test” scripts?

8) AI agent “skills” framing (agentskills.io style)

How do you want to define a “skill” in this repo?

One skill per input type? (openapi_url_to_cli, openapi_file_to_cli, html_doc_to_cli)?

What’s the intended runtime for these skills?

Local Python tool, or also runnable inside agent frameworks (CrewAI/Autogen/LangGraph)?

Should there be a standardized skill interface?

e.g., run(input: Artifact) -> GeneratedProjectArtifact

9) Quality bar & testing

What are the acceptance criteria for v1? (3–7 bullet “it’s done when…”)

What test strategy do you want?

Unit tests on parser, golden-file tests on generation, integration test calling a sample API?

Do we ship with example specs to validate generation? Which APIs? (Petstore? GitHub? Stripe?)

10) Open-source & repo setup

License preference? (MIT/Apache-2.0/GPL?)

Contribution style: do you want “good first issues”, a roadmap, RFC process?

CI requirements? (linting, formatting, type-checking, tests)

Packaging: publish to PyPI in v1 or later?

11) Safety & ethics constraints

Any guardrails?

avoid generating code that stores secrets in plaintext, warn on insecure TLS, etc. 
