---
title: "Shipment API"
source_url: "https://commerceapi.io/swagger/docs/v3"
api_version: "v3"
base_url: "https://commerceapi.io"
endpoints_count: 22
---

# Shipment API

Base URL: `https://commerceapi.io`

Endpoints: 22

---

### `GET /api/v3/Shipments`

Search shipments

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

### `POST /api/v3/Shipments`

Create a new shipment

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `Shipment` (body, string, required): The shipment to save

**Request Body:**

```
- **ShipFromAddress**: object
  The contact.
- **ShipmentDate**: string
  Gets or sets the shipment date.
- **ExpectedDeliveryDate**: string
  Gets or sets the expected delivery date.
- **InvoiceNumber**: string
  Gets or sets the invoice number.
- **BillofLading**: string
  Gets or sets the billof lading.
- **PRONumber**: string
  Gets or sets the pro number.
- **ShipmentNumber**: string
  Gets or sets the shipment number.
- **ShipmentLines**: array (required)
  Gets or sets the shipment line.
- **OrderNumber**: string
  Gets or sets the order number.
- **VendorNumber**: string
  Internal vendor number.
- **CustomerNumber**: string
  Internal customer number.
- **DepartmentNumber**: string
  Department number.
- **PartnerPO**: string
  Gets or sets the partner po.
- **SupplierPO**: string
  Gets or sets the supplier po.
- **OrderDate**: string
  Gets or sets the order date.
- **Discounts**: array
  Gets or sets the discount.
- **Taxes**: array
  Gets or sets the tax.
- **Payments**: array
  Gets or sets the payment.
- **PaymentTerm**: object
  The payment term.
- **ShipmentInfos**: array
  Gets or sets the shipment info.
- **ShipToAddress**: object
  The contact.
- **BillToAddress**: object
  The contact.
- **OrderedByAddress**: object
  The contact.
- **ExtendedAttributes**: array
  Gets or sets the extended attribute.
- **TotalAmount**: number
  Gets or sets the total amount.
- **Currency**: string
  Gets or sets the currency.
- **HandlingAmount**: number
  Gets or sets the handling amount.
- **DropshipAmount**: number
  Gets or sets the dropship fee.
- **HandlingTaxes**: array
  Gets or sets the handling tax.
- **Note**: string
  Gets or sets the note.
- **WarehouseCode**: string
  Gets or sets the warehouse code.
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

- `201`: shipment created.
- `400`: shipment data was invalid.
---

### `GET /api/v3/Shipments/ContainerCode`

Gets a new SSCC18 container code.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `containerType` (query, string, required): Container type, valid types are "box" and "pallet".

**Responses:**

- `200`: OK
---

### `POST /api/v3/Shipments/CreateImport`

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

### `POST /api/v3/Shipments/CustomXML`

Create shipment(s) based on custom XML.

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

### `POST /api/v3/Shipments/Export`

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

### `POST /api/v3/Shipments/Import`

Import from flat file.

Request rate limited to 1 request per second with bursts up to 10 requests.

**Parameters:**

- `importId` (query, string, required): Import request id
- `file` (formData, file, required): File to import

**Responses:**

- `200`: OK
---

### `GET /api/v3/Shipments/LogicbrokerKeys/Ready`

Get shipment keys that are ready for processing

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

### `GET /api/v3/Shipments/PackingSlip`

Get packing slips for multiple shipments

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `LogicbrokerKeys` (query, string, required): The logicbroker Keys.
- `fileType` (query, string, required): Valid types: jpg, png, pdf, ps, zpl

**Responses:**

- `200`: OK
---

### `POST /api/v3/Shipments/PackingSlip`

Get packing slips for a shipment before submitting

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `fileType` (query, string, required): Valid types: jpg, png, pdf, ps, zpl
- `shipment` (body, string, required): Shipment data

**Request Body:**

```
- **ShipFromAddress**: object
  The contact.
- **ShipmentDate**: string
  Gets or sets the shipment date.
- **ExpectedDeliveryDate**: string
  Gets or sets the expected delivery date.
- **InvoiceNumber**: string
  Gets or sets the invoice number.
- **BillofLading**: string
  Gets or sets the billof lading.
- **PRONumber**: string
  Gets or sets the pro number.
- **ShipmentNumber**: string
  Gets or sets the shipment number.
- **ShipmentLines**: array (required)
  Gets or sets the shipment line.
- **OrderNumber**: string
  Gets or sets the order number.
- **VendorNumber**: string
  Internal vendor number.
- **CustomerNumber**: string
  Internal customer number.
- **DepartmentNumber**: string
  Department number.
- **PartnerPO**: string
  Gets or sets the partner po.
- **SupplierPO**: string
  Gets or sets the supplier po.
- **OrderDate**: string
  Gets or sets the order date.
- **Discounts**: array
  Gets or sets the discount.
- **Taxes**: array
  Gets or sets the tax.
- **Payments**: array
  Gets or sets the payment.
- **PaymentTerm**: object
  The payment term.
- **ShipmentInfos**: array
  Gets or sets the shipment info.
- **ShipToAddress**: object
  The contact.
- **BillToAddress**: object
  The contact.
- **OrderedByAddress**: object
  The contact.
- **ExtendedAttributes**: array
  Gets or sets the extended attribute.
- **TotalAmount**: number
  Gets or sets the total amount.
- **Currency**: string
  Gets or sets the currency.
- **HandlingAmount**: number
  Gets or sets the handling amount.
- **DropshipAmount**: number
  Gets or sets the dropship fee.
- **HandlingTaxes**: array
  Gets or sets the handling tax.
- **Note**: string
  Gets or sets the note.
- **WarehouseCode**: string
  Gets or sets the warehouse code.
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

- `200`: OK
---

### `GET /api/v3/Shipments/Ready`

Get shipments that are ready for processing

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

### `GET /api/v3/Shipments/ShippingLabel`

Get shipping labels for multiple shipments

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `LogicbrokerKeys` (query, string, required): The Logicbroker keys
- `fileType` (query, string, required): Valid types: jpg, png, pdf, ps, zpl
- `containerCode` (query, string, optional): Specific container code
- `ViewInBrowser` (query, boolean, optional): Set to true to view the resulting link in the browser.

**Responses:**

- `200`: OK
---

### `POST /api/v3/Shipments/ShippingLabel`

Get shipping labels for a shipment before submitting

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `fileType` (query, string, required): Valid types: jpg, png, pdf, ps, zpl
- `shipment` (body, string, required): Shipment data
- `containerCode` (query, string, optional): Specific container code
- `ViewInBrowser` (query, boolean, optional): Set to true to view the resulting link in the browser.

**Request Body:**

```
- **ShipFromAddress**: object
  The contact.
- **ShipmentDate**: string
  Gets or sets the shipment date.
- **ExpectedDeliveryDate**: string
  Gets or sets the expected delivery date.
- **InvoiceNumber**: string
  Gets or sets the invoice number.
- **BillofLading**: string
  Gets or sets the billof lading.
- **PRONumber**: string
  Gets or sets the pro number.
- **ShipmentNumber**: string
  Gets or sets the shipment number.
- **ShipmentLines**: array (required)
  Gets or sets the shipment line.
- **OrderNumber**: string
  Gets or sets the order number.
- **VendorNumber**: string
  Internal vendor number.
- **CustomerNumber**: string
  Internal customer number.
- **DepartmentNumber**: string
  Department number.
- **PartnerPO**: string
  Gets or sets the partner po.
- **SupplierPO**: string
  Gets or sets the supplier po.
- **OrderDate**: string
  Gets or sets the order date.
- **Discounts**: array
  Gets or sets the discount.
- **Taxes**: array
  Gets or sets the tax.
- **Payments**: array
  Gets or sets the payment.
- **PaymentTerm**: object
  The payment term.
- **ShipmentInfos**: array
  Gets or sets the shipment info.
- **ShipToAddress**: object
  The contact.
- **BillToAddress**: object
  The contact.
- **OrderedByAddress**: object
  The contact.
- **ExtendedAttributes**: array
  Gets or sets the extended attribute.
- **TotalAmount**: number
  Gets or sets the total amount.
- **Currency**: string
  Gets or sets the currency.
- **HandlingAmount**: number
  Gets or sets the handling amount.
- **DropshipAmount**: number
  Gets or sets the dropship fee.
- **HandlingTaxes**: array
  Gets or sets the handling tax.
- **Note**: string
  Gets or sets the note.
- **WarehouseCode**: string
  Gets or sets the warehouse code.
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

- `200`: OK
---

### `PUT /api/v3/Shipments/Status`

Bulk update shipment status

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

### `GET /api/v3/Shipments/{LogicbrokerKey}`

Get shipment details

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `LogicbrokerKey` (path, string, required): The Logicbroker key.

**Responses:**

- `200`: OK
---

### `PUT /api/v3/Shipments/{LogicbrokerKey}`

Update shipment details

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `LogicbrokerKey` (path, string, required): The Logicbroker key
- `Shipment` (body, string, required): 

**Request Body:**

```
- **ShipFromAddress**: object
  The contact.
- **ShipmentDate**: string
  Gets or sets the shipment date.
- **ExpectedDeliveryDate**: string
  Gets or sets the expected delivery date.
- **InvoiceNumber**: string
  Gets or sets the invoice number.
- **BillofLading**: string
  Gets or sets the billof lading.
- **PRONumber**: string
  Gets or sets the pro number.
- **ShipmentNumber**: string
  Gets or sets the shipment number.
- **ShipmentLines**: array (required)
  Gets or sets the shipment line.
- **OrderNumber**: string
  Gets or sets the order number.
- **VendorNumber**: string
  Internal vendor number.
- **CustomerNumber**: string
  Internal customer number.
- **DepartmentNumber**: string
  Department number.
- **PartnerPO**: string
  Gets or sets the partner po.
- **SupplierPO**: string
  Gets or sets the supplier po.
- **OrderDate**: string
  Gets or sets the order date.
- **Discounts**: array
  Gets or sets the discount.
- **Taxes**: array
  Gets or sets the tax.
- **Payments**: array
  Gets or sets the payment.
- **PaymentTerm**: object
  The payment term.
- **ShipmentInfos**: array
  Gets or sets the shipment info.
- **ShipToAddress**: object
  The contact.
- **BillToAddress**: object
  The contact.
- **OrderedByAddress**: object
  The contact.
- **ExtendedAttributes**: array
  Gets or sets the extended attribute.
- **TotalAmount**: number
  Gets or sets the total amount.
- **Currency**: string
  Gets or sets the currency.
- **HandlingAmount**: number
  Gets or sets the handling amount.
- **DropshipAmount**: number
  Gets or sets the dropship fee.
- **HandlingTaxes**: array
  Gets or sets the handling tax.
- **Note**: string
  Gets or sets the note.
- **WarehouseCode**: string
  Gets or sets the warehouse code.
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

- `200`: OK
---

### `GET /api/v3/Shipments/{LogicbrokerKey}/EDI`

Retrieve EDI

Returns the latest EDI related to this document that was either sent or received by Logicbroker. The EDI output may also contain other documents that were in the same batch.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `LogicbrokerKey` (path, string, required): 

**Responses:**

- `200`: OK
---

### `GET /api/v3/Shipments/{LogicbrokerKey}/Events`

Retrieve related events

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `LogicbrokerKey` (path, string, required): The Logicbroker key

**Responses:**

- `200`: OK
---

### `GET /api/v3/Shipments/{LogicbrokerKey}/PackingSlip`

Get packing slips for one shipment

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `LogicbrokerKey` (path, string, required): The logicbroker Key.
- `fileType` (query, string, required): Valid types: jpg, png, pdf, ps, zpl

**Responses:**

- `200`: OK
---

### `GET /api/v3/Shipments/{LogicbrokerKey}/ShippingLabel`

Get shipping labels for one shipment.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `LogicbrokerKey` (path, string, required): The Logicbroker key.
- `fileType` (query, string, required): Valid types: jpg, png, pdf, ps, zpl
- `containerCode` (query, string, optional): Specific container code
- `ViewInBrowser` (query, boolean, optional): Set to true to view the resulting link in the browser.

**Responses:**

- `200`: OK
---

### `GET /api/v3/Shipments/{LogicbrokerKey}/status`

Get shipment status

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `LogicbrokerKey` (path, string, required): 

**Responses:**

- `200`: OK
---

### `PUT /api/v3/Shipments/{LogicbrokerKey}/status/{Status}`

Update shipment status

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `LogicbrokerKey` (path, string, required): 
- `Status` (path, string, required): 

**Responses:**

- `200`: OK
---

