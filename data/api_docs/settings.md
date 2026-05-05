---
title: "Settings API"
source_url: "https://commerceapi.io/swagger/docs/v3"
api_version: "v3"
base_url: "https://commerceapi.io"
endpoints_count: 8
---

# Settings API

Base URL: `https://commerceapi.io`

Endpoints: 8

---

### `GET /api/v3/Settings/CustomLookupTables`

Get custom lookup tables.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Responses:**

- `200`: OK
---

### `DELETE /api/v3/Settings/CustomLookupTables/{name}/Lookups`

Delete custom lookup.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `name` (path, string, required): 

**Responses:**

- `200`: OK
---

### `GET /api/v3/Settings/CustomLookupTables/{name}/Lookups`

Get custom lookup rows.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `name` (path, string, required): 

**Responses:**

- `200`: OK
---

### `POST /api/v3/Settings/CustomLookupTables/{name}/Lookups`

Create custom lookup.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `name` (path, string, required): 
- `lookup` (body, string, required): 

**Request Body:**

```
- **Id**: integer
  Custom lookup id.
- **Columns**: array
  Column values.
- **LastModified**: string
  Last modified time.
- **ModifiedBy**: string
  Last modified by.
```

**Responses:**

- `200`: OK
---

### `DELETE /api/v3/Settings/CustomLookupTables/{name}/Lookups/{id}`

Delete custom lookup.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `name` (path, string, required): 
- `id` (path, integer, required): 

**Responses:**

- `200`: OK
---

### `PUT /api/v3/Settings/CustomLookupTables/{name}/Lookups/{id}`

Update custom lookup.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `name` (path, string, required): 
- `id` (path, integer, required): 
- `lookup` (body, string, required): 

**Request Body:**

```
- **Id**: integer
  Custom lookup id.
- **Columns**: array
  Column values.
- **LastModified**: string
  Last modified time.
- **ModifiedBy**: string
  Last modified by.
```

**Responses:**

- `200`: OK
---

### `GET /api/v3/Settings/ScheduledTasks`

Get scheduled tasks.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Responses:**

- `200`: OK
---

### `PUT /api/v3/Settings/ScheduledTasks/Trigger`

Run scheduled task.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `id` (query, integer, required): Task ID

**Responses:**

- `200`: OK
---

