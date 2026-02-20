
Update the skill api-to-doc with:
- if cURL commands aren't returning useful info, try to use an MCP like Playwright or Context7 to gather info of the API.
- add tools to parse html
- try to gather request and response examples.
- try to gather info about all request params (query, path, body) and response fields to generate more complete PRD.md files. Use patterns like `Query Parameters`, `Path Parameters`, `Request Body`, `Response Body` in the documentation to identify these sections and extract details.

---
---

Update the skill skills/doc-to-prd/SKILL.md with the following content:
- create a template PRD.md file in `skills/doc-to-prd/references/PRD_template.md` with the structure and sections like:
    - Introduction
    - Installation
    - Configuration
    - Authentication
    - Endpoint Reference (with subsections for each resource, including method, path, description, parameters, response, and code examples)
    - Input/Output Examples
    - Caching
    - Rate Limiting
    - Error Handling
    - Logging
    - Best click Practices
- specify in the PRD to:
    - use uvicorn as CLI project management tool
    - add a Makefile for basic CLI commands like calling a few endpoints, running tests, and generating the PRD.md file

---
---

Update the skill skills/prd-to-cli/SKILL.md with the following content:
- add in askUserQuestion to choose between requests, httpx, or other Python HTTP libraries
- by default, src/config.py
- add a Makefile to the generated project with common commands like `make test`, `make lint`, and `make install`, and a few examples of different enpoints with GET, POS, PUT mehotds, like `make ENDPOINT_NAME-get`.
- by default log only to screen
- if log to file is selected, log to `logs/tronscan_cli_{timestamp}.log`
- when endpoint returns simple nested entities like: Get /api/account returns:
```json
{
  "data": {
    "id": 123,
    "name": "Example",
    "details": {
      "field1": "value1",
      "field2": "value2"
    }
  }
}
```
- flatten the output to accounts.json with dot notation for nested fields, like:
```json{
    "id": 123,
  "name": "Example",
  "details.field1": "value1",
  "details.field2": "value2"
}
```
- split the output to data.xlsx in different sheets, like:
```
- Sheet1 (accounts):
| id  | name    |
| --- | ------- |
| 123 | Example |
- Sheet2 (account_details):
| accounts | field1 | field2 |
| -------- | -------------- | -------------- |
| 123      | value1        | value2        |
| 456      | value3        | value4        |
```


- Ask me anything fast-paced to add triggers metadata to the YAML front matter of all three core skills when the skill should NOT be executed.
- Add a section at then end of the SKILL.md files to specify next possible steps (running skills in sequence)

in doc-to-prd, the output PRD.md file should be renamed as {project_name}_PRD.md, and the project name should be extracted from the documentation if possible, or asked to the user if not found.

can you find the created PRD.md files, and create a basic template to be used in the doc-to-prd skill? The template should include common sections and nice-to-have, with placeholders, to be filled by the skill in execution time.

why example_CLIs/restcountries-cli wasn't created without the use of 'uv' and without a pyproject.toml file?. Add a template of the pyproject.toml file to the prd-to-cli skill assets, and make sure to include it in the generated project for the CLI.

Act as a Python senior developer and analyse python files in the example_CLIs/ folder to identify improvements and bugs, and without fixing them, add such findings to the PRD.md template as a checklist of things to consider when implementing the CLI client. 

See `example_CLIs/` folder if there are more common files that could be templated for the generated projects, like a config.py file, or a utils.py file, or a logging setup file, test files, etc. Add templates for those files in the prd-to-cli skill assets, and make sure to include them in the generated project for the CLI.