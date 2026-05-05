---
title: "Acknowledgement API"
source_url: "https://commerceapi.io/swagger/docs/v3"
api_version: "v3"
base_url: "https://commerceapi.io"
endpoints_count: 14
---

# Acknowledgement API

Base URL: `https://commerceapi.io`

Endpoints: 14

---

### `GET /api/v3/Acknowledgements`

Search acknowledgements

Request rate limited to 1 request every 2 seconds with bursts up to 25 requests.

**Parameters:**

- `Filters.partnerPO` (query, string, optional): The partner's purchase order number.
- `Filters.sourceKey` (query, string, optional): Source key is usually the unique key the sender uses to find this document. Sometime this might be the same as the PartnerPO.
- `Filters.status` (query, string, optional): The status of the document. Use Status endpoint to view valid Statuses.
- `Filters.from` (query, string, optional): Beginning of time search window.
- `Filters.to` (query, string, optional): End of time search window.
- `Filters.page` (query, integer, optional): Page number
- `Filters.pageSize` (query, integer, optional): Page size
- `Filters.receiverCompanyId` (query, integer, optional): This Id is indicate who is received this document. Use the Partner endpoint to discovery valid company Ids.
- `Filters.senderCompanyId` (query, integer, optional): This Id is indicate who is sent this document. Use the Partner endpoint to discovery valid company Ids.
- `Filters.linkkey` (query, string, optional): The linkkey identifies a group of related documents. It ties the Order to all the Shipments and Invoices.

**Responses:**

- `200`: OK
---

### `POST /api/v3/Acknowledgements`

Create an acknowledgement

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `Acknowledgement` (body, string, required): Acknowledgement object

**Request Body:**

```
- **ShipToAddress**: object
  The contact.
- **BillToAddress**: object
  The contact.
- **ShipFromAddress**: object
  The contact.
- **Type**: integer enum=[0, 1, 2, 3]
  Acknowledgement type.
- **AcknowledgementNumber**: string
  Acknowledgement number.
- **OrderNumber**: string
  Original order number.
- **OrderDate**: string
  Original order date.
- **PartnerPO**: string
  Partner PO number.
- **VendorNumber**: string
  Vendor number/identifier.
- **ChangeReason**: string
  Reason for rejecting or accepting with changes.
- **AcknowledgementDate**: string
  Gets or sets the acknowledgement date.
- **ScheduledShipDate**: string
  Gets or sets the scheduled shipment date.
- **RequestedShipDate**: string
  Gets or sets the requested ship date.
- **DoNotShipBefore**: string
  Gets or sets the do not ship before date.
- **DoNotShipAfter**: string
  Gets or sets the do not ship after date.
- **ExpectedDeliveryDate**: string
  Gets or sets the expected delivery date.
- **UpdateRequestNumber**: string
  Unique identifier for an order update request.
- **ExtendedAttributes**: array
  Gets or sets the extended attribute.
- **AckLines**: array (required)
  Gets or sets the acknowledgement lines.
- **SenderCompanyId**: integer
  Gets or sets the company CoId.
- **ReceiverCompanyId**: integer
  Gets or sets the partner company CoId.
- **Identifier**: object
  The entity identifier.
- **DocumentDate**: string
  Gets or sets the document date.
- **StatusCode**: integer
  Gets or sets the status.
```

**Responses:**

- `201`: Acknowledgement created.
- `400`: Acknowledgement data was invalid.
---

### `POST /api/v3/Acknowledgements/CreateImport`

Generate import link.

This endpoint returns a temporary URL which accepts a file upload. Any column mappings sent in the request will be applied to the uploaded file.

Request rate limited to 1 request every 10 seconds with bursts up to 10 requests.

**Parameters:**

- `request` (body, string, required): 

**Request Body:**

```
- **Columns**: array
  Fields to import.
- **Delimiter**: string
  Delimiter for CSV files.
- **FileType**: string
  File type to import. Valid options are csv and xlsx.
- **DryRun**: boolean
  Return parsed results without importing anything.
- **Custom**: boolean
  False for standard format or if using the Columns field, true if using custom mapping configured by Logicbroker
```

**Responses:**

- `200`: OK
---

### `POST /api/v3/Acknowledgements/CustomXML`

Create acknowledgement(s) based on custom XML.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `xmlType` (query, string, optional): XML type, leave blank unless directed otherwise.
- `file` (formData, file, optional): File to upload
- `data` (body, string, optional): XML data to upload

**Request Body:**

```
object
```

**Responses:**

- `200`: OK
---

### `POST /api/v3/Acknowledgements/Export`

Export to CSV/XLSX

You must specify a value for either the 'LogicbrokerKeys' parameter or the 'Filter' parameter within the request.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `request` (body, string, required): Document filter, columns to export and file type.

**Request Body:**

```
- **Columns**: array
  Fields to export.
- **Filter**: object
  The lb search filter.
- **LogicbrokerKeys**: array
  List of documents to export if not using a filter.
- **Delimiter**: string
  Delimiter for CSV files.
- **FileType**: string
  File type to export. Valid options are csv, xlsx, xml and json.
```

**Responses:**

- `200`: OK
---

### `POST /api/v3/Acknowledgements/Import`

Import from flat file.

Request rate limited to 1 request per second with bursts up to 10 requests.

**Parameters:**

- `importId` (query, string, required): Import request id
- `file` (formData, file, required): File to import

**Responses:**

- `200`: OK
---

### `GET /api/v3/Acknowledgements/LogicbrokerKeys/Ready`

Get acknowledgement keys that are ready for processing

Request rate limited to 2 requests per second with bursts up to 25 requests.

**Parameters:**

- `filters.partnerPO` (query, string, optional): The partner's purchase order number.
- `filters.sourceKey` (query, string, optional): Source key is usually the unique key the sender uses to find this document. Sometime this might be the same as the PartnerPO.
- `filters.status` (query, string, optional): The status of the document. Use Status endpoint to view valid Statuses.
- `filters.from` (query, string, optional): Beginning of time search window.
- `filters.to` (query, string, optional): End of time search window.
- `filters.page` (query, integer, optional): Page number
- `filters.pageSize` (query, integer, optional): Page size
- `filters.receiverCompanyId` (query, integer, optional): This Id is indicate who is received this document. Use the Partner endpoint to discovery valid company Ids.
- `filters.senderCompanyId` (query, integer, optional): This Id is indicate who is sent this document. Use the Partner endpoint to discovery valid company Ids.
- `filters.linkkey` (query, string, optional): The linkkey identifies a group of related documents. It ties the Order to all the Shipments and Invoices.

**Responses:**

- `200`: OK
---

### `GET /api/v3/Acknowledgements/Ready`

Get acknowledgements that are ready for processing

Request rate limited to 1 request every 2 seconds with bursts up to 25 requests.

**Parameters:**

- `filters.partnerPO` (query, string, optional): The partner's purchase order number.
- `filters.sourceKey` (query, string, optional): Source key is usually the unique key the sender uses to find this document. Sometime this might be the same as the PartnerPO.
- `filters.status` (query, string, optional): The status of the document. Use Status endpoint to view valid Statuses.
- `filters.from` (query, string, optional): Beginning of time search window.
- `filters.to` (query, string, optional): End of time search window.
- `filters.page` (query, integer, optional): Page number
- `filters.pageSize` (query, integer, optional): Page size
- `filters.receiverCompanyId` (query, integer, optional): This Id is indicate who is received this document. Use the Partner endpoint to discovery valid company Ids.
- `filters.senderCompanyId` (query, integer, optional): This Id is indicate who is sent this document. Use the Partner endpoint to discovery valid company Ids.
- `filters.linkkey` (query, string, optional): The linkkey identifies a group of related documents. It ties the Order to all the Shipments and Invoices.

**Responses:**

- `200`: OK
---

### `POST /api/v3/Acknowledgements/Request`

Request an acknowledgement from a trading partner

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `Acknowledgement` (body, string, required): Acknowledgement request object

**Request Body:**

```
- **ShipToAddress**: object
  The contact.
- **BillToAddress**: object
  The contact.
- **ShipFromAddress**: object
  The contact.
- **Type**: integer enum=[0, 1, 2, 3]
  Acknowledgement type.
- **AcknowledgementNumber**: string
  Acknowledgement number.
- **OrderNumber**: string
  Original order number.
- **OrderDate**: string
  Original order date.
- **PartnerPO**: string
  Partner PO number.
- **VendorNumber**: string
  Vendor number/identifier.
- **ChangeReason**: string
  Reason for rejecting or accepting with changes.
- **AcknowledgementDate**: string
  Gets or sets the acknowledgement date.
- **ScheduledShipDate**: string
  Gets or sets the scheduled shipment date.
- **RequestedShipDate**: string
  Gets or sets the requested ship date.
- **DoNotShipBefore**: string
  Gets or sets the do not ship before date.
- **DoNotShipAfter**: string
  Gets or sets the do not ship after date.
- **ExpectedDeliveryDate**: string
  Gets or sets the expected delivery date.
- **UpdateRequestNumber**: string
  Unique identifier for an order update request.
- **ExtendedAttributes**: array
  Gets or sets the extended attribute.
- **AckLines**: array (required)
  Gets or sets the acknowledgement lines.
- **SenderCompanyId**: integer
  Gets or sets the company CoId.
- **ReceiverCompanyId**: integer
  Gets or sets the partner company CoId.
- **Identifier**: object
  The entity identifier.
- **DocumentDate**: string
  Gets or sets the document date.
- **StatusCode**: integer
  Gets or sets the status.
```

**Responses:**

- `201`: Acknowledgement request created.
- `400`: Acknowledgement data was invalid.
---

### `PUT /api/v3/Acknowledgements/Status`

Bulk update acknowledgement status

Request rate limited to 1 request per second with bursts up to 25 requests.

**Parameters:**

- `request` (body, string, required): Bulk update request

**Request Body:**

```
- **Status**: string
  New status.
- **OnlyIncreaseStatus**: boolean
  If set to true only documents in an earlier status than the one provided will be updated.
- **LogicbrokerKeys**: array
  Logicbroker keys of documents to update.
```

**Responses:**

- `200`: OK
---

### `GET /api/v3/Acknowledgements/{LogicbrokerKey}`

Get acknowledgement details

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `LogicbrokerKey` (path, string, required): 

**Responses:**

- `200`: OK
---

### `GET /api/v3/Acknowledgements/{LogicbrokerKey}/EDI`

Retrieve EDI

Returns the latest EDI related to this document that was either sent or received by Logicbroker. The EDI output may also contain other documents that were in the same batch.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `LogicbrokerKey` (path, string, required): The Logicbroker key

**Responses:**

- `200`: OK
---

### `GET /api/v3/Acknowledgements/{LogicbrokerKey}/Status`

Retrieve acknowledgement status

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `LogicbrokerKey` (path, string, required): The Logicbroker Key.

**Responses:**

- `200`: OK
---

### `PUT /api/v3/Acknowledgements/{LogicbrokerKey}/Status/{Status}`

Update acknowledgement status

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `LogicbrokerKey` (path, string, required): The Logicbroker Key.
- `Status` (path, string, required): The Status.

**Responses:**

- `200`: OK
---

