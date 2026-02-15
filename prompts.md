Update the skill skills/doc-to-prd/SKILL.md with the following content:
- use async python library for requests like httpx
- specify in the PRD to:
    - use uvicorn as CLI project management tool
    - add a Makefile for basic CLI commands like calling a few endpoints, running tests, and generating the PRD.md file
- specify in the PRD to use uvicorn as CLI project management tool


Update the skill api-to-doc with:
- if cURL commands aren't returning useful info, try to use an MCP like Playwright or Context7 to gather info of the API.
- add tools to parse html
- try to gather request and response examples.
- try to gather info about all request params (query, path, body) and response fields to generate more complete PRD.md files. Use patterns like `Query Parameters`, `Path Parameters`, `Request Body`, `Response Body` in the documentation to identify these sections and extract details.
