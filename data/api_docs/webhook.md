---
title: "Webhook API"
source_url: "https://commerceapi.io/swagger/docs/v3"
api_version: "v3"
base_url: "https://commerceapi.io"
endpoints_count: 6
---

# Webhook API

Base URL: `https://commerceapi.io`

Endpoints: 6

---

### `GET /api/v3/Webhooks`

Get list of webhooks

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Responses:**

- `200`: OK
---

### `POST /api/v3/Webhooks`

Create a new webhook

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `Webhook` (body, string, required): The new webhook.

**Request Body:**

```
- **Id**: integer
- **Format**: string (required)
- **Address**: string (required)
- **Topic**: string (required)
- **Enabled**: boolean
- **CreatedAt**: string
- **UpdatedAt**: string
- **SharedSecret**: string
```

**Responses:**

- `200`: OK
---

### `DELETE /api/v3/Webhooks/{WebhookId}`

Delete a webhook.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `WebhookId` (path, integer, required): The webhook id.

**Responses:**

- `200`: OK
---

### `GET /api/v3/Webhooks/{WebhookId}`

Get webhook details

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `WebhookId` (path, integer, required): The webhook id.

**Responses:**

- `200`: OK
---

### `PUT /api/v3/Webhooks/{WebhookId}`

Update a webhook

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `WebhookId` (path, integer, required): The webhook id.
- `Webhook` (body, string, required): The webhook.

**Request Body:**

```
- **Id**: integer
- **Format**: string (required)
- **Address**: string (required)
- **Topic**: string (required)
- **Enabled**: boolean
- **CreatedAt**: string
- **UpdatedAt**: string
- **SharedSecret**: string
```

**Responses:**

- `200`: OK
---

### `GET /api/v3/Webhooks/{WebhookId}/Test`

Test a webhook endpoint.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `WebhookId` (path, integer, required): The webhook id.
- `LogicbrokerKey` (query, string, optional): The key for a test document.

**Responses:**

- `200`: OK
---

