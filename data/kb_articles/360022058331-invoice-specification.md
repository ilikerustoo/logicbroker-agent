---
title: "Invoice Specification"
url: "https://support.logicbroker.com/kb/logicbroker/360022058331-invoice-specification"
category: "Document Standards"
---

March 10, 2026

# Invoice Specification

## 

[🔗Logicbroker_Invoice_CSV_Samples.zip](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Invoice_CSV_Samples.zip?hsLang=en) (1 KB)  
---  
[🔗Logicbroker_Invoice_JSON_Sample.json](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Invoice_JSON_Sample.json?hsLang=en) (3 KB)  
🔗[Logicbroker_810_Specs and Samples.zip](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_810_Specs%20and%20Samples.zip?hsLang=en) (70 KB)  
[🔗Logicbroker_Invoice_XML_Samples and XSD.zip](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Invoice_XML_Samples%20and%20XSD.zip?hsLang=en) (4 KB)  
[🔗Logicbroker_810_EDI_Spec.pdf](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_810_EDI_Spec.pdf?hsLang=en) (90 KB)  
  
An Invoice document is used to provide all billing information related to an order that has been fulfilled. It will contain all line item pricing, payment terms and miscellaneous charges.

#### 🗒️Note:

If you will not be integrating the invoice document, but it is required, Logicbroker offers an **Auto-Invoice** option to create invoices automatically off of the shipment document. The **ShipmentNumber** will be used as the Invoice number and all pricing information will automatically persist from the original order. To learn more [contact us](mailto:sales@logicbroker.com).

When receiving an invoice against your order, it will effect the status of that order. If all quantities on the order are invoiced the status of the order will automatically update to **Complete** (1000). It is important that the **PartnerPO** and all **SupplierSKU** data on the invoice matches the order otherwise the invoice will be non-compliant and will not transmit. 

The structure shown below in Field Descriptions follows Logicbroker's standard schema across all document formats; this includes JSON, EDI, XML, CSV, and Portal. The EDI segments are listed next to each field to indicate what field maps to the standard 810 EDI from the Logicbroker schema.

#### ✨Tip:

If you are integrating via API and need the full model schema see our [API Console.](https://commerceapi.io)

##### Details and Sample Files

**JSON**

[ Download JSON Samples ](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Invoice_JSON_Sample.json?hsLang=en)

Click the link above to download the samples. All fields listed below reflect the model schema for the Logicbroker standard JSON. For example the snippet below would match the field name **ShipToAddress.CompanyName** in the Field Descriptions below.
    
    
      "ShipToAddress": {
        "CompanyName": "Warehouse 123"
      }
    

If there is a field that is missing in the structure you can add custom fields as an extended attribute on the header level or item level; see example below. Note when a custom field is added, you will need to notify Logicbroker to ensure it is mapped to your partners.
    
    
        "ExtendedAttributes": [
        {
          "Name": "EXAMPLE",
          "Value": "Portal"
        },
        {
          "Name": "EXAMPLE2",
          "Value": "New Value"
        }
      ]
    

The value in the field descriptions documentation will show as **ExtendedAttribute.EXAMPLE** and for line items **InvoiceLine.ExtendedAttribute.EXAMPLE**.

#### 🚚For Suppliers:

To learn more about how to integrate sending invoices using the JSON format see this [link](/kb/logicbroker/360022057591-Step-6-Testing-Your-Integration?hsLang=en).

#### 👥For Retailers:

To learn more about how to integrate receiving invoices from your partners using the JSON format see this link.

**XML**

[Download XML Samples + XSD](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Invoice_XML_Samples%20and%20XSD.zip?hsLang=en)

Click the link above to download the samples and XSD. All fields listed below reflect the model schema for the Logicbroker standard XML. For example the snippet below would match the field name **ShipToAddress.CompanyName** in the Field Descriptions below.
    
    
      <ShipToAddress>
        <CompanyName>Merchant Co</CompanyName>
      </ShipToAddress>
    

If there is a field that is missing in the structure you can add custom fields as an extended attribute on the header level or item level; see example below. Note when a custom field is added, you will need to notify Logicbroker to ensure it is mapped to your partners.
    
    
      <ExtendedAttributes>
        <ExtendedAttribute>
          <Name>Example</Name>
          <Value>Portal</Value>
        </ExtendedAttribute>
        <ExtendedAttribute>
          <Name>Example2</Name>
          <Value>NewValue</Value>
        </ExtendedAttribute>
      </ExtendedAttributes>
    

The value in the field descriptions documentation will show as **ExtendedAttribute.EXAMPLE** and for line items **InvoiceLine.ExtendedAttribute.EXAMPLE**.

#### 🚚For Suppliers:

To learn more about how to integrate sending invoices using the XML format see this [link](/kb/logicbroker/360022057591-Step-6-Testing-Your-Integration?hsLang=en).

#### 👥For Retailers:

To learn more about how to integrate receiving invoices from your partners using the XML format see this link.

**EDI**

[Download EDI Specs and Samples](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_810_Specs%20and%20Samples.zip?hsLang=en)

Click the link above to download the standard 810 specification and samples. All fields listed below reflect the model schema for the Logicbroker standard XML. For example the snippet below would match the EDI field name **N102 (ST) - ShipToAddress.CompanyName** in the Field Descriptions below. The value in the parenthesis (ST) will represent the qualifier in the previous element; in this case its N101.
    
    
    N1*ST*Merchant Co~
    

For EDI fields in a loop, such as line items the will be identified by being separated with a "**:** " for example **IT1:PID05 (08)** would be represented below. "**IT1:** " indicates the element is under the **IT1** loop. **PID05** identifies the element value and again "**(08)** " within the parenthesis represents the related qualifier of "**08** " present in **PID02**. 
    
    
    IT1*1*14*EA*9*PE*VN*1234567*IN*V-123123*UP*0123456789012
    **PID*F*08***Pants~**
    IT1*2*3*EA*4*PE*VN*1234568*IN*V-123124*UP*0123456789013
    **PID*F*08***Tee Shirt~**

#### 🚚For Suppliers:

To learn more about how to integrate sending invoices using the EDI format see this [link](/kb/logicbroker/360022057591-Step-6-Testing-Your-Integration?hsLang=en).

#### 👥For Retailers:

To learn more about how to integrate receiving invoices from your partners using the EDI format see this link.

**CSV**

[Download CSV Samples](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Invoice_CSV_Samples.zip?hsLang=en)

Click the link above to download the CSV samples. Note by default if you are retrieving shipments from Logicbroker's SFTP/FTP a simplified version will be provided, the sample will be annotated with **EXPORT**.

To receive the format as listed below in the Field Descriptions, please contact [support@logicbroker.com](mailto:support@logicbroker.com). All fields listed below reflect the model schema for the Logicbroker standard API format. For example the snippet below would match the field name **ShipToAddress.CompanyName** in the Field Descriptions below.
    
    
    Id,ShipToAddress.CompanyName
    221804,Merchant Co
    

If there is a field that is missing in the structure you can add custom fields as an extended attribute on the header level or item level; see example below. Note when a custom field is added, you will need to notify Logicbroker to ensure it is mapped to your partners.
    
    
    Id,ExtendedAttribute[Name=EXAMPLE].Value
    221804,Portal
    

The value in the field descriptions documentation will show as **ExtendedAttribute.EXAMPLE** and for line items **InvoiceLine.ExtendedAttributes.EXAMPLE**

#### ✨Tip:

When submitting or receiving a **CSV** invoice, each row will be split out for each line item. If you are submitting an invoice to Logicbroker for creation, the line items will get consolidated into one invoice if they share the same **InvoiceNumber** and **PartnerPO**.

#### 🚚For Suppliers:

To learn more about how to integrate sending invoices using the CSV format see this [link](/kb/logicbroker/360022057591-Step-6-Testing-Your-Integration?hsLang=en).

#### 👥For Retailers:

To learn more about how to integrate receiving invoices from your partners using the CSV format see this link.

#### 🗒️Note:

Logicbroker has the ability to create custom specifications for any format and file type. Please [contact us](mailto:sales@logicbroker.com) and attach any samples of your custom format and we can quickly and easily implement it.

##### Field Descriptions

EDI Field | Logicbroker Field | Description | Requirement  
---|---|---|---  
N/A |  **Identifier.SourceKey** |  Identifier that will come from the source system; typically this will match the PartnerPO. |  **Read Only**  
N/A |  **Identifier.LogicbrokerKey** |  ID to identify the document in the logicbroker system. |  **Read Only**  
N/A |  **Identifier.LinkKey** |  Used to link the document to the original source document. For example, It is best to supply the Order's linkkey when posting a shipment. This will make sure the order shipped quanitites are updated on the original order and all statuses are updated appropriateley. |  **Optional**  
N/A |  **SenderCompanyId** |  Logicbroker Internal Company ID to specify what company is sending the document. |  **Required**  
N/A |  **ReceiverCompanyId** |  Logicbroker Internal Company ID to specify what company is to receive the document. |  **Required**  
BIG01 |  **InvoiceDate** |  Date of the invoice. |  **Required**  
BIG02 |  **InvoiceNumber** |  Number to identify the unique invoice document. |  **Required**  
N/A |  **DocumentDate** |  |  **Read Only**  
BIG03 |  **OrderDate** |  Date on the Purchase Order |  **Optional - will be pulled from original order if not provided**  
BIG04 |  **PartnerPO** |  This will be the purchase order number, this will be the main Key to link all your documents. This should match the order. |  **Required**  
CUR02 (SE) |  **Currency** |  Currency code to identify all values on the invoice. If no value is provided "USD" will be assumed. |  **Optional**  
SAC05 (C*G821) |  **HandlingAmount** |  Shipping and handling total to be charged on the invoice, this is part of the invoice total. |  **Optional**  
TDS02 |  **InvoiceTotal** |  Invoice total includes, full amount to be paid including line totals, shipping, taxes and discounts. Will be automatically calculated if no value is provided. |  **Required**  
REF02 (CO) |  **OrderNumber** |  Contains the end customer's order number, this will be used on the packing slip. |  **Optional**  
REF02 (IA) |  **VendorNumber** |  This is the internal vendor number provided to the supplier from the merchant. If available it is always recommended to send. |  **Optional**  
N9:MSG01 (L1*Notes) |  **Note** |  This will include any important internal messages or notes on the invoice. |  **Optional**  
SAC05 (A*C310) |  **Discounts.DiscountAmount** |  Will include the total discount, and will be used to calculate the invoice total. |  **Optional**  
ITD03 |  **Discounts.DiscountPercent** |  Discount percent will be used as part of the payment terms. It will be used with the discount due date and discount days due. |  **Optional - will be pulled from original order if not provided**  
SAC05 (C*H850) |  **Taxes.TaxAmount** |  This will be the an tax amount used to calculate the invoice total amount. |  **Optional**  
ITD04 |  **PaymentTerm.DiscountDueDate** |  Discount due date when discount will be applied. |  **Optional - will be pulled from original order if not provided**  
ITD05 |  **PaymentTerm.DiscountInNumberOfDays** |  Discount days due when discount will be applied. |  **Optional - will be pulled from original order if not provided**  
N/A |  **PaymentTerm.EffectiveDate** |  Date when the Payment terms begin. |  **Optional**  
ITD06 |  **PaymentTerm.DueDate** |  Date in which the invoice is due, before additional charges are accrued. |  **Optional - will be pulled from original order if not provided**  
ITD07 |  **PaymentTerm.PayInNumberOfDays** |  Number of days in which the invoice is due, before additional charges are accrued. |  **Optional - will be pulled from original order if not provided**  
ITD08 |  **PaymentTerm.AvailableDiscount** |  The total amount of discount available if the terms are met. |  **Optional**  
ITD12 |  **PaymentTerm.TermsDescription** |  Description of the payment terms. This will be a free form description. |  **Optional**  
N102 (RI) |  **RemitToAddress.CompanyName** |  Remit to address is only required if you do not have a business rule setup to default your remit to address. |  **Required**  
N201 (RI) |  **RemitToAddress.FirstName** |  |  **Optional**  
N202 (RI) |  **RemitToAddress.LastName** |  |  **Optional**  
N301 (RI) |  **RemitToAddress.Address1** |  |  **Required**  
N302 (RI) |  **RemitToAddress.Address2** |  |  **Optional**  
N401 (RI) |  **RemitToAddress.City** |  |  **Required**  
N402 (RI) |  **RemitToAddress.State** |  |  **Required**  
N404 (RI) |  **RemitToAddress.Country** |  |  **Required**  
N403 (RI) |  **RemitToAddress.Zip** |  |  **Required**  
N104 (RI*92) |  **RemitToAddress.AddressCode** |  |  **Optional**  
N1:PER06 (TE) |  **RemitToAddress.Phone** |  |  **Optional**  
N1:PER04 (EM) |  **RemitToAddress.Email** |  |  **Optional**  
SAC05 (A*ZZZZ) |  **ExtendedAttribute.Allowance - ZZZ** |  Used to indicate an additional detailed allowance. The Code as shown in the example ZZZ will correspond to what type of allowance. See specific partner details for the applicable codes. These will be deducted automatically in the invoice total calculation. |  **Optional**  
SAC05 (C*ZZZZ) |  **ExtendedAttribute.Charge - ZZZ** |  Used to indicate an additional detailed charge. The Code as shown in the example ZZZ will correspond to what type of charge. See specific partner details for the applicable codes. These will be added automatically in the invoice total calculation. |  **Optional**  
IT101 |  **InvoiceLine.LineNumber** |  Line Number from the Order. If not provided this will be taked from the order automatically. |  **Required**  
IT104 |  **InvoiceLine.Price** |  Unit cost that the merchant is being billed for that line. |  **Required**  
IT105 |  **InvoiceLine.PriceCode** |  Used to indicate the price level for the product. See specific partner details for applicable codes. |  **Optional**  
IT102 |  **InvoiceLine.Quantity** |  Contains the quantity of items to be invoiced. |  **Required**  
IT103 |  **InvoiceLine.QuantityUOM** |  Unit of Measure for the quantity invoiced. See partner's details for specifics. |  **Required**  
IT1:PID05 (08) |  **InvoiceLine.Description** |  Standard short description or name of the product. |  **Optional**  
IT109 (IN) |  **InvoiceLine.ItemIdentifier.PartnerSKU** |  The Item identifier that is internal to the purchaser/merchant. |  **Conditional - if received on an order this value should be returned**  
IT107 (VN) |  **InvoiceLine.ItemIdentifier.SupplierSKU** |  The Item Identifier that is used by the supplier or the person fulfilling the product. This will always contain a value. |  **Required**  
IT110 (UP) |  **InvoiceLine.ItemIdentifier.UPC** |  Typically the U.P.C Consumer Package code will be provided; however additional standardized codes can be provided here as well. See specific partner instructions for details. |  **Conditional - if received on an order this value should be returned**  
IT1:SAC05 (C*H850) |  **InvoiceLine.Taxes.TaxAmount** |  Item Level Tax amount |  **Optional**