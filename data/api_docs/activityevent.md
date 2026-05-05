---
title: "ActivityEvent API"
source_url: "https://commerceapi.io/swagger/docs/v3"
api_version: "v3"
base_url: "https://commerceapi.io"
endpoints_count: 4
---

# ActivityEvent API

Base URL: `https://commerceapi.io`

Endpoints: 4

---

### `GET /api/v3/ActivityEvents`

Get events for given fitlers

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `Filters.from` (query, string, optional): Beginning of time search window.
- `Filters.to` (query, string, optional): End of time search window.
- `Filters.linkKey` (query, string, optional): The linkkey identifies a group of related documents.
- `Filters.logicbrokerKey` (query, integer, optional): Logicbroker document identifier.
- `Filters.documentType` (query, string, optional): Document type.
- `Filters.typeId` (query, integer, optional): Event type identifier.
- `Filters.category` (query, string, optional): Event category.
- `Filters.level` (query, string, optional): Event level (Info, Alert, etc.)
- `Filters.page` (query, integer, optional): Page number.
- `Filters.senderId` (query, integer, optional): Event sender.
- `Filters.receiverId` (query, integer, optional): Event receiver.
- `Filters.processed` (query, boolean, optional): Processed flag.
- `Filters.viewed` (query, boolean, optional): Viewed flag.

**Responses:**

- `200`: OK
---

### `GET /api/v3/ActivityEvents/EventTypes`

Gets a list of all possible event types.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Responses:**

- `200`: OK
---

### `GET /api/v3/ActivityEvents/{EventId}`

Gets the event with the specified id.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `EventId` (path, string, required): The id to search for.

**Responses:**

- `200`: OK
---

### `PUT /api/v3/ActivityEvents/{EventId}`

Update activity event

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `EventId` (path, integer, required): The Event Id.
- `activityEvent` (body, string, required): The updated activityEvent

**Request Body:**

```
- **Id**: integer
  Gets or sets the id.
- **Date**: string
  Gets or sets the event date.
- **SenderId**: integer
  Gets or sets the id of the company sending the event.
- **ReceiverId**: integer
  Gets or sets the id of the company receiving the vent.
- **LogicbrokerKey**: integer
  Gets or sets the Logicbroker key for the document this event relates to, if applicable.
- **DocumentType**: string
  Gets or sets the document type for the document this event relates to, if applicable.
- **LinkKey**: string
  Gets or sets the link-key key for the document this event relates to, if applicable.
- **TypeId**: integer
  Gets or sets the event type id.
- **Level**: string
  Gets or sets the event level.
- **Category**: string
  Gets or sets the event category.
- **Summary**: string
  Gets or sets the summary.
- **Details**: string
  Gets or sets the details.
- **Processed**: boolean
  Gets or sets a value indicating whether processed.
- **Viewed**: boolean
  Gets or sets a value indicating whether viewed.
- **AdditionalData**: string
  JSON encoded string for extra properties.
```

**Responses:**

- `200`: OK
---

