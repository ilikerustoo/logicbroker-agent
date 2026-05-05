---
title: "Message API"
source_url: "https://commerceapi.io/swagger/docs/v3"
api_version: "v3"
base_url: "https://commerceapi.io"
endpoints_count: 7
---

# Message API

Base URL: `https://commerceapi.io`

Endpoints: 7

---

### `GET /api/v3/Messages`

Get messages.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `page` (query, integer, optional): Page
- `pageSize` (query, integer, optional): Page size

**Responses:**

- `200`: OK
---

### `POST /api/v3/Messages`

Create new message.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `message` (body, string, required): Message details

**Request Body:**

```
- **Subject**: string
  Message subject
- **Body**: string
  Message body
- **ReceiverIds**: array
  Receiver account numbers
- **RequireAcknowledgement**: boolean
  True if acknowledgement is required
- **DocId**: integer
  Associated doc id
- **Status**: string
  Thread status
- **IsPrivate**: boolean
  True if message should be hidden from end customer
- **CustomerId**: string
  External customer id
```

**Responses:**

- `200`: OK
---

### `GET /api/v3/Messages/Export`

Export messages.

Request rate limited to 1 request per second with bursts up to 5 requests.

**Parameters:**

- `fileType` (query, string, optional): CSV or XLSX.

**Responses:**

- `200`: OK
---

### `GET /api/v3/Messages/{messageId}/Acknowledgements`

Get receipt information for a message.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `messageId` (path, integer, required): Message id

**Responses:**

- `200`: OK
---

### `POST /api/v3/Messages/{messageId}/Acknowledgements`

Acknowledge a message if needed.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `messageId` (path, integer, required): Message id

**Responses:**

- `200`: OK
---

### `GET /api/v3/Messages/{messageId}/Replies`

Get replies to a message.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `messageId` (path, integer, required): Message id
- `page` (query, integer, optional): Page
- `pageSize` (query, integer, optional): Page size

**Responses:**

- `200`: OK
---

### `POST /api/v3/Messages/{messageId}/Replies`

Reply to a message.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `messageId` (path, integer, required): Message id
- `reply` (body, string, required): Reply details

**Request Body:**

```
- **Body**: string
  Message body
- **ReplyTo**: integer
  Id of parent message if any
- **DocId**: integer
  Associated doc ID
- **IsPrivate**: boolean
  True if reply should be hidden from end customer
- **CustomerId**: string
  External customer id
```

**Responses:**

- `200`: OK
---

