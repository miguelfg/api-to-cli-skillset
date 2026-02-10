# API Documentation Standards Comparison v2


## 1. **OpenAPI Specification (OAS)**

**Formerly:** Swagger

* **Format:** YAML / JSON
* **Link:** [https://spec.openapis.org/oas/latest.html](https://spec.openapis.org/oas/latest.html)

### ✅ Includes

* Endpoints & HTTP methods
* Request parameters (path, query, header, cookie)
* Request/response bodies
* Status codes
* Authentication & authorization (OAuth2, API keys, JWT, etc.)
* Schemas (via JSON Schema subset)
* Examples
* Server environments

### ❌ Does NOT Include

* Business logic rules
* Database structure
* Performance SLAs
* Async/event-driven flows (partially hackable, but not native)
* UI/UX behavior

---

## 2. **AsyncAPI**

**For event-driven & messaging APIs**

* **Format:** YAML / JSON
* **Link:** [https://www.asyncapi.com/docs/reference/specification/latest](https://www.asyncapi.com/docs/reference/specification/latest)

### ✅ Includes

* Channels (topics, queues, streams)
* Published/subscribed messages
* Message payload schemas
* Brokers (Kafka, MQTT, AMQP, WebSockets, etc.)
* Security schemes
* Message examples

### ❌ Does NOT Include

* REST endpoints
* Synchronous request/response semantics
* UI flows
* Database models

---

## 3. **GraphQL Schema Definition Language (SDL)**

* **Format:** GraphQL SDL (`.graphql`)
* **Link:** [https://graphql.org/learn/schema/](https://graphql.org/learn/schema/)

### ✅ Includes

* Object types
* Queries, mutations, subscriptions
* Field arguments
* Type relationships
* Descriptions (docstrings)

### ❌ Does NOT Include

* HTTP details (status codes, headers)
* Auth mechanisms (out-of-band)
* Caching rules
* Transport-level behavior

---

## 4. **gRPC + Protocol Buffers**

**Strongly typed RPC APIs**

* **Format:** `.proto` files
* **Link:**

  * [https://grpc.io/docs/](https://grpc.io/docs/)
  * [https://protobuf.dev/](https://protobuf.dev/)

### ✅ Includes

* Services & RPC methods
* Message schemas
* Streaming semantics (unary, server/client/bidirectional)
* Strong typing
* Auto-generated client/server code

### ❌ Does NOT Include

* REST semantics
* Human-readable docs by default
* Authentication policies (defined externally)
* Error semantics beyond status codes

---

## 5. **RAML (RESTful API Modeling Language)**

* **Format:** YAML
* **Link:** [https://raml.org/specs/raml-10](https://raml.org/specs/raml-10)

### ✅ Includes

* REST endpoints
* Methods & parameters
* Reusable traits & resource types
* Request/response bodies
* Examples

### ❌ Does NOT Include

* Async/event-driven APIs
* Runtime behavior
* Performance or SLA guarantees

---

## 6. **API Blueprint**

* **Format:** Markdown (`.md`)
* **Link:** [https://apiblueprint.org/documentation/specification.html](https://apiblueprint.org/documentation/specification.html)

### ✅ Includes

* Endpoints & methods
* Request/response examples
* Status codes
* Human-readable narrative

### ❌ Does NOT Include

* Formal schema validation
* Strong typing
* Code generation (limited)
* Async patterns

---

## 7. **JSON Schema**

**Schema, not a full API spec**

* **Format:** JSON
* **Link:** [https://json-schema.org/specification](https://json-schema.org/specification)

### ✅ Includes

* Field types
* Required vs optional fields
* Constraints (min/max, patterns, enums)
* Validation rules

### ❌ Does NOT Include

* Endpoints
* HTTP methods
* Authentication
* API flows

👉 Often embedded inside **OpenAPI** or **AsyncAPI**

---

## 8. **JSON:API**

**Opinionated REST response format**

* **Format:** JSON
* **Link:** [https://jsonapi.org/format/](https://jsonapi.org/format/)

### ✅ Includes

* Standardized response structure
* Resource relationships
* Pagination, filtering, sorting conventions
* Error object format

### ❌ Does NOT Include

* Endpoint definitions
* Auth specs
* Non-REST APIs
* Async behavior

---

## 9. **HAL (Hypertext Application Language)**

* **Format:** JSON or XML
* **Link:** [https://stateless.group/hal_specification.html](https://stateless.group/hal_specification.html)

### ✅ Includes

* Hypermedia links
* Embedded resources
* HATEOAS-style navigation

### ❌ Does NOT Include

* Schema definitions
* Validation rules
* Full API descriptions

---

## 10. **WSDL (SOAP APIs)**

* **Format:** XML
* **Link:** [https://www.w3.org/TR/wsdl20/](https://www.w3.org/TR/wsdl20/)

### ✅ Includes

* Operations
* Input/output messages
* Data types (XSD)
* Transport bindings

### ❌ Does NOT Include

* REST semantics
* JSON support
* Modern developer ergonomics

---

## 🔍 Quick Comparison

| Standard        | Style       | Human-Readable | Code Gen | Async      |
| --------------- | ----------- | -------------- | -------- | ---------- |
| OpenAPI         | REST        | ✔              | ✔        | ⚠️ Partial |
| AsyncAPI        | Events      | ✔              | ✔        | ✔          |
| GraphQL SDL     | GraphQL     | ✔              | ✔        | ✔          |
| gRPC / Protobuf | RPC         | ❌              | ✔✔       | ✔          |
| RAML            | REST        | ✔              | ✔        | ⚠️         |
| API Blueprint   | REST        | ✔✔             | ❌        | ❌          |
| JSON Schema     | Data        | ❌              | ✔        | N/A        |
| JSON:API        | REST format | ✔              | ❌        | ❌          |
| WSDL            | SOAP        | ❌              | ✔        | ❌          |

---

## 🧠 Rule of Thumb

* **Public REST API:** OpenAPI
* **Internal microservices:** gRPC
* **Event-driven data pipelines:** AsyncAPI
* **Frontend-heavy apps:** GraphQL
* **Strict response consistency:** JSON:API

