---
title: "Document API"
source_url: "https://commerceapi.io/swagger/docs/v3"
api_version: "v3"
base_url: "https://commerceapi.io"
endpoints_count: 4
---

# Document API

Base URL: `https://commerceapi.io`

Endpoints: 4

---

### `GET /api/v3/Document/Script/{ScriptName}`

Execute custom handler.

Request rate limited to 1 request every 5 seconds with bursts up to 25 requests.

**Parameters:**

- `ScriptName` (path, string, required): The custom script name.

**Responses:**

- `200`: OK
---

### `OPTIONS /api/v3/Document/Script/{ScriptName}`

Execute custom handler.

Request rate limited to 1 request every 5 seconds with bursts up to 25 requests.

**Parameters:**

- `ScriptName` (path, string, required): The custom script name.

**Responses:**

- `200`: OK
---

### `POST /api/v3/Document/Script/{ScriptName}`

Execute custom handler.

Request rate limited to 1 request every 5 seconds with bursts up to 25 requests.

**Parameters:**

- `ScriptName` (path, string, required): The custom script name.

**Responses:**

- `200`: OK
---

### `GET /api/v3/Document/Search`

Search documents.

Request rate limited to 2 requests per second with bursts up to 10 requests.

**Parameters:**

- `filter` (query, string, optional): A way to refine your search results using OData query options. For example, Type eq 'Order' and StatusCode lt 500
- `term` (query, string, optional): The term you are using to search by such as SKU, shipping address, product name, etc.
- `page` (query, integer, optional): Page number
- `pageSize` (query, integer, optional): Page size
- `orderBy` (query, string, optional): The way you are reviewing the returned results. For example, Date asc

**Responses:**

- `200`: OK
---

