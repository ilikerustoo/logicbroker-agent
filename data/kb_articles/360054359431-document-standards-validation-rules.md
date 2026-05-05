---
title: "Document Standards (Validation Rules)"
url: "https://support.logicbroker.com/kb/logicbroker/360054359431-document-standards-validation-rules"
category: "Platform"
---

March 5, 2026

# Document Standards (Validation Rules)

## 

**Audience:** Suppliers are able to use view document standards directly from the Logicbroker portal. Retailers should work with Logicbroker to configure these depending on their document requirements.

In this article, you will find information related to Document Standards and what is required for the document to pass validation. The sections within this article are outlined below:

  * Overview
  * Navigating to Document Standards
  * Document Standards Defined
  * How to Use This Tool
  * Related Content



### Overview 

Suppliers have the ability to review document standards required when connecting with Retailers prior to submitting orders, acknowledgments, shipments, invoices, returns, or inventory. Retailers are able to work with Logicbroker to configure these requirements. This tool serves as validation, where required fields and their descriptions are showcased directly in the Portal. 

### Navigating to Documents Standards in the Portal 

To view the document standards, navigate to the left-hand side toolbar, and select **Retailers (or Suppliers)**. Select **Document Standards** from the dropdown that appears.

### Document Standards Defined

The required field is the first piece of information, followed by the requirement, and the details around that field requirement. The information provided in the details should be applied to the document. 

**Definitions**

**Company **– Since the data changes depending on which partner a supplier is working with, a dropdown is available (if they have multiple retail partners) to select what data they are looking at. Once a retail partner has been selected, suppliers can view the validation rules for the document of their choice.

**Documents** As seen from the image above, validation rules are available for orders, acknowledgements, shipments, invoices, returns, and inventory. The documents are shown at the top of the page directly under the Validation Rules header. Click on the document to view the associated requirements.

**Field **– This is the field of the document. For example, AckLines.Quantity on an acknowledgement or ShipmentNumber on a shipment. 

**Required **– This is where a supplier can see if a field is required or not. If this box has a red check mark, the field is mandatory for the document to be successfully transmitted.

**Description **– The description provides more details about what is required for the document to be successful. This could be something as simple as the ShipmentNumber description or complex like the AckLinesChangeReason description (both shown below).

  *     * ShipmentNumber - This is used as a unique value to identify your shipment. This will be used to prevent sending duplicate shipments.
    * AckLinesChangeReason - If AckLines.QuantityCancelled is greater than 0, the following codes will need to be provided: All codes listed will map from standard change reasons in Logicbroker. ID = merchant_request (Maps from "Administrative request", "Cancelled at retailer's request", or "Other") IF = info_missing (Maps from "Info missing on purchase order")



_**Please Note:** _Some of the required fields may be generated automatically by Logicbroker which will be indicated in the description, others will be more detailed providing all of the information needed to successfully send the document.

### How to Use This Tool

Let's say, for example, a supplier is sending a shipment and is unsure how the shipment number is used and if it is a requirement. After pulling up the validation rules for their partner, the supplier can see that the ShipmentNumber field (1) is required because of the red checkmark (2). The information also tells the supplier that the ShipmentNumber is used to identify shipments and prevent sending duplicate shipments (3). 

This tool allows users to review exactly what is needed to send documents to their partners, what it means, and to help reduce failures when transmitting documents.