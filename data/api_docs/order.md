---
title: "Order API"
source_url: "https://commerceapi.io/swagger/docs/v3"
api_version: "v3"
base_url: "https://commerceapi.io"
endpoints_count: 24
---

# Order API

Base URL: `https://commerceapi.io`

Endpoints: 24

---

### `GET /api/v3/Orders`

Search orders

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

### `POST /api/v3/Orders`

Create an order

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `SalesOrder` (body, string, required): Order object

**Request Body:**

```
- **RequestedShipDate**: string
  Gets or sets the requested ship date.
- **DoNotShipBefore**: string
  Gets or sets the do not ship before date.
- **DoNotShipAfter**: string
  Gets or sets the do not ship after date.
- **ExpectedDeliveryDate**: string
  Gets or sets the expected delivery date.
- **ShipFromAddress**: object
  The contact.
- **RemitToAddress**: object
  The contact.
- **MarkForAddress**: object
  The contact.
- **TypeCode**: string
  Purchase order type code.
- **ReleaseNumber**: string
  Purchase order release number.
- **SalesRequirement**: integer enum=[0, 1, 2]
  Sales requirement, used to allow/prevent backorders
- **OrderLines**: array (required)
  Gets or sets the order line.
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

- `201`: Order created.
- `400`: Order data was invalid.
---

### `POST /api/v3/Orders/CreateImport`

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

### `POST /api/v3/Orders/CustomXML`

Create order(s) based on custom XML.

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

### `POST /api/v3/Orders/Export`

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

### `POST /api/v3/Orders/Import`

Import from flat file.

Request rate limited to 1 request per second with bursts up to 10 requests.

**Parameters:**

- `importId` (query, string, required): Import request id
- `file` (formData, file, required): File to import

**Responses:**

- `200`: OK
---

### `GET /api/v3/Orders/LogicbrokerKeys/Ready`

Get order keys that are ready for processing

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

### `GET /api/v3/Orders/PickList`

Get pick lists for multiple orders

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `LogicbrokerKeys` (query, string, required): The logicbroker Keys.
- `FileType` (query, string, required): Valid types: jpg, png, pdf, ps, zpl
- `ViewInBrowser` (query, boolean, optional): Set to true to view the resulting link in the browser.

**Responses:**

- `200`: OK
---

### `GET /api/v3/Orders/Ready`

Get orders that are ready for processing

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

### `PUT /api/v3/Orders/Status`

Bulk update order status

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

### `GET /api/v3/Orders/{LogicbrokerKey}`

Retrieve an order

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `LogicbrokerKey` (path, string, required): The Logicbroker Key.

**Responses:**

- `200`: OK
---

### `GET /api/v3/Orders/{LogicbrokerKey}/ActivityEvents`

Retrieve related events

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `LogicbrokerKey` (path, string, required): The Logicbroker key

**Responses:**

- `200`: OK
---

### `GET /api/v3/Orders/{LogicbrokerKey}/EDI`

Retrieve EDI

Returns the latest EDI related to this document that was either sent or received by Logicbroker. The EDI output may also contain other documents that were in the same batch.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `LogicbrokerKey` (path, string, required): The Logicbroker key

**Responses:**

- `200`: OK
---

### `GET /api/v3/Orders/{LogicbrokerKey}/Invoices`

Retrieve a list of invoices for an order

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `LogicbrokerKey` (path, string, required): The Logicbroker key

**Responses:**

- `200`: OK
---

### `POST /api/v3/Orders/{LogicbrokerKey}/Invoices`

Creates invoice and links with the given order

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `LogicbrokerKey` (path, string, required): The Logicbroker Key.
- `Invoice` (body, string, required): The invoice.

**Request Body:**

```
- **RemitToAddress**: object
  The contact.
- **ShipFromAddress**: object
  The contact.
- **InvoiceLines**: array (required)
  Gets or sets the invoice line.
- **InvoiceNumber**: string (required)
  Gets or sets the invoice number.
- **InvoiceDate**: string
  Gets or sets the invoice date.
- **InvoiceTotal**: number
  Gets or sets the invoice total.
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

- `201`: Invoice created.
- `400`: Invoice data was invalid.
---

### `GET /api/v3/Orders/{LogicbrokerKey}/PickList`

Get pick list for one order

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `LogicbrokerKey` (path, string, required): The logicbroker Key.
- `FileType` (query, string, required): Valid types: jpg, png, pdf, ps, zpl
- `ViewInBrowser` (query, boolean, optional): Set to true to view the resulting link in the browser.

**Responses:**

- `200`: OK
---

### `GET /api/v3/Orders/{LogicbrokerKey}/Returns`

Retrieve a list of returns for an order

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `LogicbrokerKey` (path, string, required): The Logicbroker key

**Responses:**

- `200`: OK
---

### `POST /api/v3/Orders/{LogicbrokerKey}/Returns`

The create return for sales order.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `LogicbrokerKey` (path, string, required): The Logicbroker Key.
- `Return` (body, string, required): The shipment.

**Request Body:**

```
- **ShipToAddress**: object
  The contact.
- **BillToAddress**: object
  The contact.
- **ShipFromAddress**: object
  The contact.
- **OrderedByAddress**: object
  The contact.
- **ReturnNumber**: string (required)
  Return number.
- **ReturnDate**: string
  Gets or sets the return date.
- **OrderNumber**: string
  Original order number.
- **OrderDate**: string
  Original order date.
- **PartnerPO**: string
  Partner PO number.
- **VendorNumber**: string
  Vendor number/identifier.
- **Note**: string
  Notes.
- **ExtendedAttributes**: array
  Gets or sets the extended attribute.
- **ReturnLines**: array (required)
  Gets or sets the return lines.
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

- `201`: Return created.
- `400`: Return data was invalid.
---

### `GET /api/v3/Orders/{LogicbrokerKey}/Shipments`

Retrieve a list of shipments for an order

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `LogicbrokerKey` (path, string, required): The Logicbroker key

**Responses:**

- `200`: OK
---

### `POST /api/v3/Orders/{LogicbrokerKey}/Shipments`

The create shipment for sales order.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `LogicbrokerKey` (path, string, required): The Logicbroker Key.
- `Shipment` (body, string, required): The shipment.

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

- `201`: Shipment created.
- `400`: Shipment data was invalid.
---

### `GET /api/v3/Orders/{LogicbrokerKey}/ShippingOptions`

Get shipping/tracking label options.

Request rate limited to 2 requests per second with bursts up to 25 requests.

**Parameters:**

- `LogicbrokerKey` (path, string, required): The Logicbroker key

**Responses:**

- `200`: OK
---

### `GET /api/v3/Orders/{LogicbrokerKey}/Status`

Retrieve order status

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `LogicbrokerKey` (path, string, required): The Logicbroker Key.

**Responses:**

- `200`: OK
---

### `PUT /api/v3/Orders/{LogicbrokerKey}/Status/{Status}`

Update order status

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `LogicbrokerKey` (path, string, required): The Logicbroker Key.
- `Status` (path, string, required): The Status.

**Responses:**

- `200`: OK
---

### `POST /api/v3/Orders/{LogicbrokerKey}/TrackingLabel`

Generate a tracking label for a given package

Request rate limited to 2 requests per second with bursts up to 25 requests.

**Parameters:**

- `LogicbrokerKey` (path, string, required): The Logicbroker key
- `package` (body, string, required): Package details
- `useSenderAccount` (query, boolean, required): Set to true to use the sender's shipping account

**Request Body:**

```
- **Package**: object
  The shipment info.
- **ShipFromAddress**: object
  The contact.
- **Items**: array
  Package items
```

**Responses:**

- `200`: OK
---

