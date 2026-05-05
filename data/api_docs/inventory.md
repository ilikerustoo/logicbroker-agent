---
title: "Inventory API"
source_url: "https://commerceapi.io/swagger/docs/v3"
api_version: "v3"
base_url: "https://commerceapi.io"
endpoints_count: 13
---

# Inventory API

Base URL: `https://commerceapi.io`

Endpoints: 13

---

### `POST /api/v3/Inventory/All/Export`

Export inventory as CSV/XLSX for all partners.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `request` (body, string, required): Export settings

**Request Body:**

```
- **Delimiter**: string
  Delimiter for CSV files.
- **FileType**: string
  Export file type (csv or xlsx).
- **Filter**: object
  Conditions for performing advanced field mapping.
- **IncludeNullQuantity**: boolean
  Set to true to include items with null quantity.
- **Mapped**: boolean
  Set to false to view items with no merchant SKU.
- **ModifiedAfter**: string
  Only items modified after this time.
- **Transform**: boolean
  Transform output (if configured).
```

**Responses:**

- `200`: OK
---

### `GET /api/v3/Inventory/Availability/{sku}`

Get the availability of an item across all suppliers.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `sku` (path, string, required): Merchant SKU

**Responses:**

- `200`: OK
---

### `POST /api/v3/Inventory/Broadcast`

Import inventory from CSV.

Request rate limited to 1 request every 60 seconds with bursts up to 2 requests.

**Parameters:**

- `transform` (query, boolean, optional): Transform CSV (if configured)
- `file` (formData, file, required): File to import

**Responses:**

- `200`: OK
---

### `DELETE /api/v3/Inventory/{partnerId}`

Delete all inventory records.

Request rate limited to 1 request every 60 seconds with bursts up to 2 requests.

**Parameters:**

- `partnerId` (path, integer, required): Partner account number

**Responses:**

- `200`: OK
---

### `GET /api/v3/Inventory/{partnerId}`

Download inventory as CSV.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `partnerId` (path, integer, required): Partner account number
- `modifiedAfter` (query, string, optional): Only items modified after this time
- `mapped` (query, boolean, optional): Set to false to view items with no merchant SKU
- `transform` (query, boolean, optional): Transform CSV (if configured)
- `includeNullQuantity` (query, boolean, optional): Set to true to include items with null quantity
- `fileType` (query, string, optional): CSV or XLSX

**Responses:**

- `200`: OK
---

### `POST /api/v3/Inventory/{partnerId}`

Import inventory from CSV.

Request rate limited to 1 request every 10 seconds with bursts up to 30 requests.

**Parameters:**

- `partnerId` (path, integer, required): Partner account number
- `transform` (query, boolean, optional): Transform CSV (if configured)
- `file` (formData, file, optional): File to import (CSV/XLSX)
- `data` (body, string, optional): Inventory in JSON format

**Request Body:**

```
object
```

**Responses:**

- `200`: OK
---

### `POST /api/v3/Inventory/{partnerId}/Export`

Export inventory as CSV/XLSX for a partner.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `partnerId` (path, integer, required): Partner id
- `request` (body, string, required): Export settings

**Request Body:**

```
- **Delimiter**: string
  Delimiter for CSV files.
- **FileType**: string
  Export file type (csv or xlsx).
- **Filter**: object
  Conditions for performing advanced field mapping.
- **IncludeNullQuantity**: boolean
  Set to true to include items with null quantity.
- **Mapped**: boolean
  Set to false to view items with no merchant SKU.
- **ModifiedAfter**: string
  Only items modified after this time.
- **Transform**: boolean
  Transform output (if configured).
```

**Responses:**

- `200`: OK
---

### `GET /api/v3/Inventory/{partnerId}/Item/{sku}`

Get a single item by SKU

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `partnerId` (path, integer, required): Partner account number
- `sku` (path, string, required): Item SKU

**Responses:**

- `200`: OK
---

### `GET /api/v3/Inventory/{partnerId}/Match/{sku}`

Get a single item by merchant SKU

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `partnerId` (path, integer, required): Partner account number
- `sku` (path, string, required): Item SKU

**Responses:**

- `200`: OK
---

### `DELETE /api/v3/Inventory/{partnerId}/Matching`

Delete all SKU mappings.

Request rate limited to 1 request every 60 seconds with bursts up to 2 requests.

**Parameters:**

- `partnerId` (path, integer, required): Partner account number

**Responses:**

- `200`: OK
---

### `POST /api/v3/Inventory/{partnerId}/Matching`

Match items with CSV.

Request rate limited to 1 request every 10 seconds with bursts up to 10 requests.

**Parameters:**

- `partnerId` (path, integer, required): Partner account number
- `file` (formData, file, required): File to import

**Responses:**

- `200`: OK
---

### `PUT /api/v3/Inventory/{partnerId}/Resend`

Resend all inventory items.

Request rate limited to 1 request every 5 minutes with bursts up to 2 requests.

**Parameters:**

- `partnerId` (path, integer, required): Partner account number

**Responses:**

- `200`: OK
---

### `PUT /api/v3/Inventory/{partnerId}/ZeroOut`

Set all inventory quantity to zero.

Request rate limited to 1 request every 5 minutes with bursts up to 2 requests.

**Parameters:**

- `partnerId` (path, integer, required): Partner account number

**Responses:**

- `200`: OK
---

