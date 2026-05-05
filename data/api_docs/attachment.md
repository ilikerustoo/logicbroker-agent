---
title: "Attachment API"
source_url: "https://commerceapi.io/swagger/docs/v3"
api_version: "v3"
base_url: "https://commerceapi.io"
endpoints_count: 3
---

# Attachment API

Base URL: `https://commerceapi.io`

Endpoints: 3

---

### `GET /api/v3/Attachments`

Get a list of all attachments matching a given filter.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `type` (query, string, optional): Attachment type
- `receiverId` (query, integer, optional): Receiver account number
- `logicbrokerKey` (query, integer, optional): Logicbroker key
- `acknowledged` (query, boolean, optional): Acknowledged flag
- `page` (query, integer, optional): Page number

**Responses:**

- `200`: OK
---

### `POST /api/v3/Attachments`

Upload an attachment

Request rate limited to 1 request every 5 seconds with bursts up to 10 requests.

**Parameters:**

- `type` (query, string, required): Attachment type (json, xml, csv, txt, pdf, png)
- `receiverId` (query, integer, optional): Receiver account number
- `logicbrokerKeys` (query, string, optional): Logicbroker document keys to attach
- `description` (query, string, optional): Attachment description
- `url` (query, string, optional): URL of file to attach
- `file` (formData, file, optional): File to attach
- `data` (body, string, optional): XML/JSON data to attach (webhooks)

**Request Body:**

```
object
```

**Responses:**

- `200`: OK
---

### `GET /api/v3/Attachments/{container}/{name}`

Retrieve a file from Logicbroker storage.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `container` (path, string, required): File container (ex. edidocs, attachments)
- `name` (path, string, required): File name

**Responses:**

- `200`: OK
---

