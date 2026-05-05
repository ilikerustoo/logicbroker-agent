---
title: "Product API"
source_url: "https://commerceapi.io/swagger/docs/v3"
api_version: "v3"
base_url: "https://commerceapi.io"
endpoints_count: 47
---

# Product API

Base URL: `https://commerceapi.io`

Endpoints: 47

---

### `DELETE /api/v3/Product/AttributeSets`

Remove all attribute sets.

Request rate limited to 1 request every 60 seconds with bursts up to 2 requests.

**Responses:**

- `200`: OK
---

### `GET /api/v3/Product/AttributeSets`

Get catalog attribute sets.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Responses:**

- `200`: OK
---

### `POST /api/v3/Product/AttributeSets`

Create catalog attribute set.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `attributeSet` (body, string, required): Attribute set details

**Request Body:**

```
- **Name**: string (required)
  Internal attribute set id.
- **FriendlyName**: string (required)
  Attribute set label.
- **Attributes**: array
  Attribute names.
- **Tags**: string
  List of tags.
- **Hidden**: boolean
  True if attribute set is hidden.
- **HiddenFromPartner**: boolean
  True if attribute set is hidden from partners.
- **DestinationId**: string
  Attribute identifier in destination system.
- **CustomAttributes**: string
  Custom attributes if any.
- **SyncStatus**: string
  Sync status with destination system.
- **System**: boolean
  True if attribute set is a built-in value.
- **LastModified**: string
  Last modified date.
```

**Responses:**

- `200`: OK
---

### `DELETE /api/v3/Product/AttributeSets/{name}`

Delete catalog attribute set.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `name` (path, string, required): Attribute set name

**Responses:**

- `204`: No Content
---

### `PUT /api/v3/Product/AttributeSets/{name}`

Update catalog attribute set.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `name` (path, string, required): Attribute set name
- `attributeSet` (body, string, required): Attribute set details

**Request Body:**

```
- **Name**: string (required)
  Internal attribute set id.
- **FriendlyName**: string (required)
  Attribute set label.
- **Attributes**: array
  Attribute names.
- **Tags**: string
  List of tags.
- **Hidden**: boolean
  True if attribute set is hidden.
- **HiddenFromPartner**: boolean
  True if attribute set is hidden from partners.
- **DestinationId**: string
  Attribute identifier in destination system.
- **CustomAttributes**: string
  Custom attributes if any.
- **SyncStatus**: string
  Sync status with destination system.
- **System**: boolean
  True if attribute set is a built-in value.
- **LastModified**: string
  Last modified date.
```

**Responses:**

- `200`: OK
---

### `DELETE /api/v3/Product/Attributes`

Remove all attributes.

Request rate limited to 1 request every 60 seconds with bursts up to 2 requests.

**Responses:**

- `200`: OK
---

### `GET /api/v3/Product/Attributes`

Get catalog attributes.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Responses:**

- `200`: OK
---

### `POST /api/v3/Product/Attributes`

Create catalog attribute.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `attribute` (body, string, required): Attribute details

**Request Body:**

```
- **Name**: string (required)
  Internal attribute id.
- **FriendlyName**: string (required)
  Attribute label.
- **Type**: string (required)
  Attribute type.
- **Description**: string
  Attribute description.
- **Options**: array
  Available options.
- **Group**: string (required)
  Attribute group.
- **System**: boolean
  True if attribute is a built-in value.
- **Tags**: string
  List of tags.
- **Hidden**: boolean
  True if attribute is hidden.
- **HiddenFromPartner**: boolean
  True if attribute is hidden from partners.
- **DestinationId**: string
  Attribute identifier in destination system.
- **CustomAttributes**: string
  Custom attributes if any.
- **SyncStatus**: string
  Sync status with destination system.
- **Editor**: string
  Editor type. Leave blank for default.
- **ValidationRules**: array
  Validation rules.
- **LastModified**: string
  Last modified date.
```

**Responses:**

- `200`: OK
---

### `DELETE /api/v3/Product/Attributes/{name}`

Delete catalog attribute.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `name` (path, string, required): Attribute name

**Responses:**

- `204`: No Content
---

### `PUT /api/v3/Product/Attributes/{name}`

Update catalog attribute.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `name` (path, string, required): Attribute name
- `attribute` (body, string, required): Attribute details

**Request Body:**

```
- **Name**: string (required)
  Internal attribute id.
- **FriendlyName**: string (required)
  Attribute label.
- **Type**: string (required)
  Attribute type.
- **Description**: string
  Attribute description.
- **Options**: array
  Available options.
- **Group**: string (required)
  Attribute group.
- **System**: boolean
  True if attribute is a built-in value.
- **Tags**: string
  List of tags.
- **Hidden**: boolean
  True if attribute is hidden.
- **HiddenFromPartner**: boolean
  True if attribute is hidden from partners.
- **DestinationId**: string
  Attribute identifier in destination system.
- **CustomAttributes**: string
  Custom attributes if any.
- **SyncStatus**: string
  Sync status with destination system.
- **Editor**: string
  Editor type. Leave blank for default.
- **ValidationRules**: array
  Validation rules.
- **LastModified**: string
  Last modified date.
```

**Responses:**

- `200`: OK
---

### `DELETE /api/v3/Product/Categories`

Remove all categories.

Request rate limited to 1 request every 60 seconds with bursts up to 2 requests.

**Responses:**

- `200`: OK
---

### `GET /api/v3/Product/Categories`

Get categories.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Responses:**

- `200`: OK
---

### `POST /api/v3/Product/Categories`

Create category.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `category` (body, string, required): Category details

**Request Body:**

```
- **Id**: string
  Category id.
- **ParentId**: string
  Parent category id.
- **Hidden**: boolean
  Hide in category list.
- **HiddenFromPartner**: boolean
  Hide from partners.
- **Name**: string (required)
  Category name.
- **DestinationId**: string
  Identifier in destination system.
- **BannerURL**: string
  Banner URL.
- **CustomAttributes**: string
  Custom attributes.
- **SyncStatus**: string
  Sync status with destination.
- **Position**: integer
  Position among sibling categories.
- **Level**: integer
  Level in category tree.
- **Children**: integer
  Number of children.
- **Path**: string
  Full category path.
- **AttributeSet**: string (required)
  Attribute set name.
- **LastModified**: string
  Last modified time.
```

**Responses:**

- `200`: OK
---

### `DELETE /api/v3/Product/Categories/{id}`

Delete category.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `id` (path, string, required): Category id

**Responses:**

- `204`: No Content
---

### `PUT /api/v3/Product/Categories/{id}`

Update category.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `id` (path, string, required): Category id
- `category` (body, string, required): Category details

**Request Body:**

```
- **Id**: string
  Category id.
- **ParentId**: string
  Parent category id.
- **Hidden**: boolean
  Hide in category list.
- **HiddenFromPartner**: boolean
  Hide from partners.
- **Name**: string (required)
  Category name.
- **DestinationId**: string
  Identifier in destination system.
- **BannerURL**: string
  Banner URL.
- **CustomAttributes**: string
  Custom attributes.
- **SyncStatus**: string
  Sync status with destination.
- **Position**: integer
  Position among sibling categories.
- **Level**: integer
  Level in category tree.
- **Children**: integer
  Number of children.
- **Path**: string
  Full category path.
- **AttributeSet**: string (required)
  Attribute set name.
- **LastModified**: string
  Last modified time.
```

**Responses:**

- `200`: OK
---

### `POST /api/v3/Product/Exports/AttributeSets`

Export attribute sets as CSV/XLSX.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `request` (body, string, required): Export settings

**Request Body:**

```
- **Delimiter**: string
  Delimiter for CSV files.
- **FileType**: string
  Export file type (csv or xlsx).
- **Columns**: array
  Column mappings, omit to export all columns in the catalog.
- **Rules**: array
  Rules to run on the catalog before column mappings.
- **Filter**: object
  Conditions for performing advanced field mapping.
- **AcceptCachedValues**: boolean
  Accept values that may be a few minutes out of date for better performance.
```

**Responses:**

- `200`: OK
---

### `POST /api/v3/Product/Exports/Attributes`

Export attributes as CSV/XLSX.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `request` (body, string, required): Export settings

**Request Body:**

```
- **Delimiter**: string
  Delimiter for CSV files.
- **FileType**: string
  Export file type (csv or xlsx).
- **Columns**: array
  Column mappings, omit to export all columns in the catalog.
- **Rules**: array
  Rules to run on the catalog before column mappings.
- **Filter**: object
  Conditions for performing advanced field mapping.
- **AcceptCachedValues**: boolean
  Accept values that may be a few minutes out of date for better performance.
```

**Responses:**

- `200`: OK
---

### `POST /api/v3/Product/Exports/Categories`

Export categories as CSV/XLSX.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `request` (body, string, required): Export settings

**Request Body:**

```
- **Delimiter**: string
  Delimiter for CSV files.
- **FileType**: string
  Export file type (csv or xlsx).
- **Columns**: array
  Column mappings, omit to export all columns in the catalog.
- **Rules**: array
  Rules to run on the catalog before column mappings.
- **Filter**: object
  Conditions for performing advanced field mapping.
- **AcceptCachedValues**: boolean
  Accept values that may be a few minutes out of date for better performance.
```

**Responses:**

- `200`: OK
---

### `POST /api/v3/Product/Exports/Products`

Export products as CSV/XLSX.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `request` (body, string, required): Export settings

**Request Body:**

```
- **Delimiter**: string
  Delimiter for CSV files.
- **FileType**: string
  Export file type (csv or xlsx).
- **Columns**: array
  Column mappings, omit to export all columns in the catalog.
- **Rules**: array
  Rules to run on the catalog before column mappings.
- **Filter**: object
  Conditions for performing advanced field mapping.
- **AcceptCachedValues**: boolean
  Accept values that may be a few minutes out of date for better performance.
```

**Responses:**

- `200`: OK
---

### `POST /api/v3/Product/Imports/AttributeSets`

Generate attribute sets import link.

This endpoint returns a temporary URL which accepts a file upload. Any column mappings sent in the request will be applied to the uploaded file.

Request rate limited to 1 request every 10 seconds with bursts up to 10 requests.

**Parameters:**

- `request` (body, string, required): 

**Request Body:**

```
- **Columns**: array
  Column mappings.
- **Rules**: array
  Rules to run on the catalog before column mappings.
```

**Responses:**

- `200`: OK
---

### `POST /api/v3/Product/Imports/AttributeSets/Upload`

Import attribute sets from token

Request rate limited to 1 request per second with bursts up to 10 requests.

**Parameters:**

- `importId` (query, string, required): 
- `file` (formData, file, required): File to import

**Responses:**

- `200`: OK
---

### `POST /api/v3/Product/Imports/Attributes`

Generate attribute import link.

This endpoint returns a temporary URL which accepts a file upload. Any column mappings sent in the request will be applied to the uploaded file.

Request rate limited to 1 request every 10 seconds with bursts up to 10 requests.

**Parameters:**

- `request` (body, string, required): 

**Request Body:**

```
- **Columns**: array
  Column mappings.
- **Rules**: array
  Rules to run on the catalog before column mappings.
```

**Responses:**

- `200`: OK
---

### `POST /api/v3/Product/Imports/Attributes/Upload`

Import attributes from token

Request rate limited to 1 request per second with bursts up to 10 requests.

**Parameters:**

- `importId` (query, string, required): 
- `file` (formData, file, required): File to import

**Responses:**

- `200`: OK
---

### `POST /api/v3/Product/Imports/Categories`

Generate category import link.

This endpoint returns a temporary URL which accepts a file upload. Any column mappings sent in the request will be applied to the uploaded file.

Request rate limited to 1 request every 10 seconds with bursts up to 10 requests.

**Parameters:**

- `request` (body, string, required): 

**Request Body:**

```
- **Columns**: array
  Column mappings.
- **Rules**: array
  Rules to run on the catalog before column mappings.
```

**Responses:**

- `200`: OK
---

### `POST /api/v3/Product/Imports/Categories/Upload`

Import categories from token

Request rate limited to 1 request per second with bursts up to 10 requests.

**Parameters:**

- `importId` (query, string, required): 
- `file` (formData, file, required): File to import

**Responses:**

- `200`: OK
---

### `POST /api/v3/Product/Imports/Products`

Generate product import link.

This endpoint returns a temporary URL which accepts a file upload. Any column mappings sent in the request will be applied to the uploaded file.

Request rate limited to 1 request every 10 seconds with bursts up to 10 requests.

**Parameters:**

- `request` (body, string, required): 

**Request Body:**

```
- **Columns**: array
  Column mappings.
- **Rules**: array
  Rules to run on the catalog before column mappings.
```

**Responses:**

- `200`: OK
---

### `GET /api/v3/Product/Imports/Products/Status`

Get status of catalog import.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `importId` (query, string, required): 

**Responses:**

- `200`: OK
---

### `POST /api/v3/Product/Imports/Products/Upload`

Import from CSV/XLSX.

Request rate limited to 1 request every 10 seconds with bursts up to 10 requests.

**Parameters:**

- `importId` (query, string, required): 
- `file` (formData, file, required): File to import

**Responses:**

- `200`: OK
---

### `GET /api/v3/Product/Products`

Get items in the catalog.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `page` (query, integer, optional): Page number
- `pageSize` (query, integer, optional): Page size
- `syncStatus` (query, string, optional): Product sync status
- `approvalStatus` (query, string, optional): Product approval status
- `parentSku` (query, string, optional): Parent SKU

**Responses:**

- `200`: OK
---

### `POST /api/v3/Product/Products`

Create a product.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `product` (body, string, required): Product details

**Request Body:**

```
- **Id**: string
  Product identifier.
- **Attributes**: object
  Product attributes.
- **LastModified**: string
  Last modified date.
- **ErrorMessage**: string
  Error message if any.
```

**Responses:**

- `200`: OK
---

### `DELETE /api/v3/Product/Products/{id}`

Delete a product.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `id` (path, string, required): Product id

**Responses:**

- `204`: No Content
---

### `GET /api/v3/Product/Products/{id}`

Get a single product.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `id` (path, string, required): Product id

**Responses:**

- `200`: OK
---

### `PUT /api/v3/Product/Products/{id}`

Update a product.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `product` (body, string, required): Product details
- `id` (path, string, required): Product id

**Request Body:**

```
- **Id**: string
  Product identifier.
- **Attributes**: object
  Product attributes.
- **LastModified**: string
  Last modified date.
- **ErrorMessage**: string
  Error message if any.
```

**Responses:**

- `200`: OK
---

### `GET /api/v3/Product/Settings`

External catalog settings

Request rate limited to 1 request per second with bursts up to 10 requests.

**Responses:**

- `200`: OK
---

### `GET /api/v3/Product/{partnerId}/AttributeSets`

Get catalog attribute sets for a partner.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `partnerId` (path, integer, required): 

**Responses:**

- `200`: OK
---

### `GET /api/v3/Product/{partnerId}/Attributes`

Get catalog attributes for a partner.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `partnerId` (path, integer, required): Partner id

**Responses:**

- `200`: OK
---

### `GET /api/v3/Product/{partnerId}/Categories`

Get categories for a partner.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `partnerId` (path, integer, required): 

**Responses:**

- `200`: OK
---

### `POST /api/v3/Product/{partnerId}/Exports/SupplierProducts`

Export products as CSV/XLSX for a partner.

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
- **Columns**: array
  Column mappings, omit to export all columns in the catalog.
- **Rules**: array
  Rules to run on the catalog before column mappings.
- **Filter**: object
  Conditions for performing advanced field mapping.
- **AcceptCachedValues**: boolean
  Accept values that may be a few minutes out of date for better performance.
```

**Responses:**

- `200`: OK
---

### `POST /api/v3/Product/{partnerId}/Imports/SupplierProducts`

Generate supplier product import link.

This endpoint returns a temporary URL which accepts a file upload. Any column mappings sent in the request will be applied to the uploaded file.

Request rate limited to 1 request every 10 seconds with bursts up to 10 requests.

**Parameters:**

- `partnerId` (path, integer, required): 
- `request` (body, string, required): 

**Request Body:**

```
- **Columns**: array
  Column mappings.
- **Rules**: array
  Rules to run on the catalog before column mappings.
```

**Responses:**

- `200`: OK
---

### `GET /api/v3/Product/{partnerId}/Imports/SupplierProducts/Status`

Get status of catalog import.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `partnerId` (path, integer, required): 
- `importId` (query, string, required): 

**Responses:**

- `200`: OK
---

### `POST /api/v3/Product/{partnerId}/Imports/SupplierProducts/Upload`

Import from CSV/XLSX.

Request rate limited to 1 request every 10 seconds with bursts up to 10 requests.

**Parameters:**

- `importId` (query, string, required): 
- `partnerId` (path, string, required): 
- `file` (formData, file, required): File to import

**Responses:**

- `200`: OK
---

### `GET /api/v3/Product/{partnerId}/Products/{id}`

Get a single product for a partner.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `partnerId` (path, integer, required): Partner id
- `id` (path, string, required): Product id

**Responses:**

- `200`: OK
---

### `GET /api/v3/Product/{partnerId}/SupplierProducts`

Get items in the supplier catalog.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `partnerId` (path, integer, required): Partner id
- `page` (query, integer, optional): Page number
- `pageSize` (query, integer, optional): Page size
- `syncStatus` (query, string, optional): Product sync status
- `approvalStatus` (query, string, optional): Product approval status
- `parentSku` (query, string, optional): Parent SKU

**Responses:**

- `200`: OK
---

### `POST /api/v3/Product/{partnerId}/SupplierProducts`

Create a product for a supplier.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `partnerId` (path, integer, required): Partner id
- `product` (body, string, required): Product details

**Request Body:**

```
- **Id**: string
  Product identifier.
- **Attributes**: object
  Product attributes.
- **LastModified**: string
  Last modified date.
- **ErrorMessage**: string
  Error message if any.
```

**Responses:**

- `200`: OK
---

### `DELETE /api/v3/Product/{partnerId}/SupplierProducts/{id}`

Delete a product for a supplier.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `partnerId` (path, integer, required): Partner id
- `id` (path, string, required): Product id

**Responses:**

- `204`: No Content
---

### `GET /api/v3/Product/{partnerId}/SupplierProducts/{id}`

Get a single product for a supplier.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `partnerId` (path, integer, required): Partner id
- `id` (path, string, required): Product id

**Responses:**

- `200`: OK
---

### `PUT /api/v3/Product/{partnerId}/SupplierProducts/{id}`

Update a product for a supplier.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `partnerId` (path, integer, required): Partner id
- `product` (body, string, required): Product details
- `id` (path, string, required): Product id

**Request Body:**

```
- **Id**: string
  Product identifier.
- **Attributes**: object
  Product attributes.
- **LastModified**: string
  Last modified date.
- **ErrorMessage**: string
  Error message if any.
```

**Responses:**

- `200`: OK
---

