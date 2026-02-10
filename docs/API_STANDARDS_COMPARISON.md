# API Documentation Standards Comparison

Here’s a concise overview of the *major API documentation standards* and specifications used today — from lightweight formats for describing REST APIs to rich ecosystems that generate interactive docs.

---

## 📘 **1. OpenAPI (formerly Swagger)**

* **What it is:** The de-facto standard for describing REST APIs.
* **Format:** YAML or JSON
* **Why it’s popular:**

  * Supports automated generation of API docs, client SDKs, and server stubs.
  * Works with tools like **Swagger UI**, **Redoc**, and many API gateways.
* **Use-case:** RESTful HTTP APIs.

```yaml
openapi: 3.1.0
info:
  title: Example API
  version: '1.0'
```

---

## 💬 **2. AsyncAPI**

* **What it is:** Standard for event-driven and asynchronous APIs (e.g., Kafka, MQTT, WebSockets).
* **Format:** YAML or JSON
* **Features:**

  * Describes event channels, message payloads, and brokers.
  * Helps generate documentation and tooling for messaging architectures.
* **Use-case:** Event streaming and async architectures.

---

## 📊 **3. GraphQL SDL (Schema Definition Language)**

* **What it is:** Official way to define GraphQL APIs.
* **Includes:** Types, queries, mutations, and subscriptions.
* **Tool ecosystem:** GraphiQL, Apollo Studio, GraphQL Playground.
* **Use-case:** GraphQL services.

---

## 🤖 **4. gRPC + Protocol Buffers (protobuf)**

* **What it is:** RPC framework with a strongly-typed IDL.
* **Format:** `.proto` files
* **Features:**

  * Defines services and messages.
  * Enables auto-generated code for many languages.
* **Use-case:** Internal services, high-performance APIs.

---

## 🧠 **5. JSON Schema**

* **What it is:** A standard for describing the *structure* of JSON data.
* **Use-case:** Can be used standalone or embedded in other specs (like OpenAPI) to validate payloads.

---

## 🌐 **6. RAML (RESTful API Modeling Language)**

* **What it is:** A YAML-based API modeling language similar to OpenAPI.
* **Features:** Focus on readability and modular design.
* **Use-case:** REST APIs, often in enterprise contexts.

---

## 🤝 **7. API Blueprint**

* **What it is:** Markdown-based API description format.
* **Tools:** Aglio, Snowboard, Dredd (for testing against blueprint).
* **Use-case:** RESTful APIs with a human-friendly doc focus.

---

## 🛠 **8. WSDL (Web Services Description Language)**

* **What it is:** XML specification for SOAP web services.
* **Use-case:** Legacy/enterprise SOAP APIs.

---

## 🧩 **9. HAL, JSON:API, Siren (Hypermedia Formats)**

* **What they are:** Conventions for hypermedia API responses.
* **Purpose:** Embed links and actions in REST responses.
* **Use-case:** HATEOAS-style APIs.

---

## 📄 **10. OpenAPI Extensions / Doc Tooling**

Standards *not formats*, but used frequently with API docs:

* **Swagger UI / Redoc:** Interactive docs from OpenAPI specs.
* **Slate / Docusaurus:** Custom developer portals.
* **Stoplight / Postman Collections:** API modeling + docs + testing.

---

## 🧠 **Quick Comparison**

| Standard        | Best For           | Format    | Async Support |
| --------------- | ------------------ | --------- | ------------- |
| OpenAPI         | REST APIs          | YAML/JSON | Partial       |
| AsyncAPI        | Event-driven       | YAML/JSON | ✔             |
| GraphQL SDL     | GraphQL APIs       | SDL       | ✔             |
| protobuf + gRPC | RPC APIs           | `.proto`  | ✔             |
| RAML            | REST APIs          | YAML      | Partial       |
| API Blueprint   | REST APIs          | Markdown  | No            |
| JSON Schema     | Payload validation | JSON      | N/A           |
| WSDL            | SOAP               | XML       | No            |

---

