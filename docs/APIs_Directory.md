# APIs Directory

This report lists **real-world APIs**, grouped by **API style / documentation standard**, with **direct links to their specifications** where available.

---

## 1. REST APIs (OpenAPI / Swagger)

### Stripe API
- **Domain:** Payments
- **Docs:** https://stripe.com/docs/api
- **OpenAPI Spec:**
  - YAML: https://github.com/stripe/openapi/blob/main/latest/spec3.yaml
  - JSON: https://github.com/stripe/openapi/blob/main/latest/spec3.json
- **Notes:** Gold-standard OpenAPI; great for codegen testing

### GitHub REST API
- **Domain:** Developer platforms
- **Docs:** https://docs.github.com/rest
- **OpenAPI Spec:**
  - https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.json
- **Notes:** Large, complex, many auth + pagination patterns

### Twilio API
- **Domain:** Messaging / Voice
- **Docs:** https://www.twilio.com/docs/usage/api
- **OpenAPI Specs:**
  - https://github.com/twilio/twilio-oai/tree/main/spec
- **Notes:** Split per product; very realistic enterprise API

### Slack Web API
- **Domain:** Collaboration
- **Docs:** https://api.slack.com/web
- **OpenAPI Spec:**
  - https://github.com/slackapi/slack-api-specs/blob/main/web_api/openapi/slack_web_api_2.json
- **Notes:** Mix of REST + events ecosystem

### Spotify Web API
- **Domain:** Media
- **Docs:** https://developer.spotify.com/documentation/web-api/
- **OpenAPI Spec:**
  - Community: https://github.com/thelinmichael/spotify-web-api-spec
- **Notes:** No official spec; good LLM parsing target

### Notion API
- **Domain:** Productivity / Knowledge management
- **Docs:** https://developers.notion.com/
- **API Reference:** https://developers.notion.com/reference/intro
- **Notes:** Strong candidate for auth, pagination, and content/database workflows

### Google Maps Platform / Places API
- **Domain:** Maps / Location search
- **Docs:** https://developers.google.com/maps/documentation/
- **Places API:** https://developers.google.com/maps/documentation/places/web-service
- **Notes:** Good for parameter-heavy search, pagination, and geospatial use cases

### National Weather Service API
- **Domain:** Weather / Government data
- **Docs:** https://www.weather.gov/documentation/services-web-api
- **Notes:** Public API with realistic weather and forecast resource patterns

### OpenWeather API
- **Domain:** Weather
- **Docs:** https://openweathermap.org/api
- **Notes:** Good mid-complexity REST target with forecast/current-condition endpoints

### TomTom APIs
- **Domain:** Maps / Routing / Traffic
- **Docs:** https://developer.tomtom.com/apis
- **Notes:** Good candidate for routing, search, and traffic-style command groups

### OpenAI API
- **Domain:** AI / Developer platform
- **Docs:** https://platform.openai.com/docs
- **Notes:** Useful for auth, polling, and modern API workflow patterns

### Plaid API
- **Domain:** Financial data / Banking connectivity
- **Docs:** https://plaid.com/docs/api/
- **Notes:** Strong sandbox-driven API with auth and resource lifecycle complexity

### Spoonacular API
- **Domain:** Food / Recipes
- **Docs:** https://spoonacular.com/food-api
- **Notes:** Good lightweight candidate for search/filter-oriented CLI workflows

### ExchangeRate.host API
- **Domain:** Finance / Exchange rates
- **Docs:** https://exchangerate.host/documentation
- **Notes:** Simple public API for fast end-to-end workflow testing

### OMDb API
- **Domain:** Movies / Metadata
- **Docs:** https://www.omdbapi.com/
- **Notes:** Small and fast API for simple smoke-test style examples

---

## 2. GraphQL APIs

### GitHub GraphQL API
- **Docs:** https://docs.github.com/graphql
- **Schema:** Introspected via endpoint
- **Notes:** Complex schema, good for future GraphQL-to-CLI support

### Shopify Storefront GraphQL
- **Docs:** https://shopify.dev/api/storefront
- **Notes:** Auth-heavy, versioned schemas

### SpaceX GraphQL (Public)
- **Endpoint:** https://api.spacex.land/graphql/
- **Notes:** Excellent demo API

---

## 3. Async / Event-Driven APIs (AsyncAPI)

### AsyncAPI Official Examples
- **Specs:** https://github.com/asyncapi/spec/tree/master/examples
- **Protocols:** Kafka, MQTT, WebSockets
- **Notes:** Canonical AsyncAPI inputs

### NATS JetStream
- **Docs:** https://docs.nats.io/jetstream
- **Notes:** Event-driven, infra-focused

---

## 4. gRPC / Protobuf APIs

### Google Cloud Pub/Sub
- **Proto Files:**
  - https://cloud.google.com/pubsub/docs/reference/rpc/google.pubsub.v1
- **Notes:** Strongly typed, streaming

### Envoy xDS APIs
- **Specs:** https://www.envoyproxy.io/docs/envoy/latest/api
- **Notes:** Advanced infra APIs

---

## 5. SOAP / WSDL APIs

### PayPal SOAP APIs
- **Docs:** https://developer.paypal.com/docs/classic/soap-api/
- **Notes:** Legacy but realistic enterprise input

### FedEx SOAP APIs
- **Docs:** https://www.fedex.com/en-us/developer.html

---

## 6. RAML APIs

### RAML Example APIs
- **Specs:** https://github.com/raml-org/raml-examples
- **Notes:** Clean RAML inputs for testing

### MuleSoft API Workshops
- **Specs:** https://github.com/MuleSoft/api-workshop

---

## 7. API Blueprint APIs

### Apiary Example APIs
- **Docs:** https://apiary.io/apis
- **Notes:** Markdown-first API descriptions

---

## 8. JSON:API-Compliant APIs

### JSON:API Examples
- **Docs:** https://jsonapi.org/examples/
- **Notes:** Strict response format rules

---

## 9. Hypermedia / HAL APIs

### GitHub REST (HAL links)
- **Docs:** https://docs.github.com/rest/overview/resources-in-the-rest-api#hypermedia

### PayPal REST
- **Notes:** Uses HAL-style links

---

## 10. Reference & Directories

- Public APIs list: https://github.com/public-apis/public-apis
- Swagger Petstore (demo): https://petstore.swagger.io

---

## Why this list matters for your project

This collection gives you:
- **High-quality OpenAPI inputs** (Stripe, Twilio)
- **Messy / community specs** (Spotify, Shopify)
- **Non-REST formats** for future skills
- **Real-world auth, pagination, rate-limit patterns**

Perfect foundation for an **AI skill that turns API docs into Python Click CLIs** 🚀
