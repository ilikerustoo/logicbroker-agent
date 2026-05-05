---
title: "Status API"
source_url: "https://commerceapi.io/swagger/docs/v3"
api_version: "v3"
base_url: "https://commerceapi.io"
endpoints_count: 2
---

# Status API

Base URL: `https://commerceapi.io`

Endpoints: 2

---

### `GET /api/v3/Statuses`

Get configured document statuses for each document

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Responses:**

- `200`: OK
---

### `GET /api/v3/Statuses/{documentType}`

Get configured document statuses for each document

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `documentType` (path, string, required): Document type

**Responses:**

- `200`: OK
---

