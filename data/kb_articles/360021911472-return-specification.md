---
title: "Return Specification"
url: "https://support.logicbroker.com/kb/logicbroker/360021911472-return-specification"
category: "Document Standards"
---

March 12, 2026

# Return Specification

## 

[🔗Logicbroker_Return_CSV_Standard_IMPORT.xlsx](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Return_CSV_Standard_IMPORT.xlsx?hsLang=en) (9 KB)  
---  
[🔗Logicbroker 180 EDI Specs and Samples.zip](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker%20180%20EDI%20Specs%20and%20Samples.zip?hsLang=en) (50 KB)  
[🔗Logicbroker_Return_JSON_Sample.json](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Return_JSON_Sample.json?hsLang=en) (942 Bytes)  
[🔗Logicbroker_Return_XML_Sample_and_XSD.zip](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Return_XML_Sample_and_XSD.zip?hsLang=en) (3 KB)  
  
A return document in the Logicbroker system is used by a supplier notifying the retailer that a return has been received. This will typically contain all products received, reason for return by the end customer, and any other RMA information.

#### ✨Tip:

Not all retailers support handling of return documents. Remember to always check with your partner if they have the ability to support returns. Logicbroker will also indicate this under testing and fail a return document if the partner cannot receive it.

When creating a return against your order, it will not effect the status of that order or any other document in the system. However, it is still important that the **PartnerPO** and all **SupplierSKU** data on the return matches the order otherwise the return will be non-compliant and will not transmit. 

The structure shown below in Field Descriptions follows Logicbroker's standard schema across all document formats; this includes JSON, EDI, XML, CSV, and Portal. The EDI segments are listed next to each field to indicate what field maps to the standard 180 EDI from the Logicbroker schema.

#### ✨Tip:

If you are integrating via API and need the full model schema see our [API Console.](https://commerceapi.io)

##### Details and Sample Files

**JSON**

[ Download JSON Samples ](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Return_JSON_Sample.json?hsLang=en)

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
    

The value in the field descriptions documentation will show as **ExtendedAttribute.EXAMPLE** and for line items **ReturnLines.ExtendedAttribute.EXAMPLE**.

#### 🚚For Suppliers:

To learn more about how to integrate sending returns using the JSON format see this [link](/kb/logicbroker/360022057591-Step-6-Testing-Your-Integration?hsLang=en).

#### 👥For Retailers:

To learn more about how to integrate receiving returns from your partners using the JSON format see this link.

**XML**

[Download XML Samples + XSD](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Return_XML_Sample_and_XSD.zip?hsLang=en)

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
    

The value in the field descriptions documentation will show as **ExtendedAttribute.EXAMPLE** and for line items **ReturnLines.ExtendedAttribute.EXAMPLE**.

#### 🚚For Suppliers:

To learn more about how to integrate sending returns using the XML format see this [link](/kb/logicbroker/360022057591-Step-6-Testing-Your-Integration?hsLang=en).

#### 👥For Retailers:

To learn more about how to integrate receiving returns from your partners using the XML format see this link.

**EDI**

[Download EDI Specs and Samples](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker%20180%20EDI%20Specs%20and%20Samples.zip?hsLang=en)

Click the link above to download the standard 180 specification and samples. All fields listed below reflect the model schema for the Logicbroker standard XML. For example the snippet below would match the EDI field name **PRF01 - PartnerPO** in the Field Descriptions below.
    
    
    PRF*1599999999~
    

For EDI fields in a loop, such as line items the will be identified by being separated with a "**:** " for example **BLI:RDR04 (DR)** would be represented below. "**BLI:** " indicates the element is under the **BLI** loop. **RDR04** identifies the element value, within the parenthesis represents the related qualifier of "**DR** " present in **RDR02**. 
    
    
    BLI*VN*V-123123*1*EA****IN*1234567*UP*0123456789012~  
    **RDR**DR**TOO SMALL~**  
     BLI*VN*V-1234568*1*EA****IN*123124*UP*0123456789013~  
    **RDR**DR**TOO BIG~**

#### 🚚For Suppliers:

To learn more about how to integrate sending returns using the EDI format see this [link](/kb/logicbroker/360022057591-Step-6-Testing-Your-Integration?hsLang=en).

#### 👥For Retailers:

To learn more about how to integrate receiving returns from your partners using the EDI format see this link.

**CSV**

[Download CSV Samples](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Return_CSV_Standard_IMPORT.xlsx?hsLang=en)

Click the link above to download the CSV samples. Note by default if you are retrieving returns from Logicbroker's SFTP/FTP a it will require setup by Logicbroker support, [contact us](mailto:support@logicbroker.com) for more information.

All fields listed below reflect the model schema for the Logicbroker standard API format. For example the snippet below would match the field name **ShipToAddress.CompanyName** in the Field Descriptions below.
    
    
    Id,ShipToAddress.CompanyName
    221804,Merchant Co
    

If there is a field that is missing in the structure you can add custom fields as an extended attribute on the header level or item level; see example below. Note when a custom field is added, you will need to notify Logicbroker to ensure it is mapped to your partners.
    
    
    Id,ExtendedAttribute[Name=EXAMPLE].Value
    221804,Portal
    

The value in the field descriptions documentation will show as **ExtendedAttribute.EXAMPLE** and for line items **ReturnLines.ExtendedAttribute.EXAMPLE**

#### ✨Tip:

When submitting or receiving a **CSV** return, each row will be split out for each line item. If you are submitting an return to Logicbroker for creation, the line items will get consolidated into one return document if they share the same **ReturnNumber** and **PartnerPO**.

#### 🚚For Suppliers:

To learn more about how to integrate sending returns using the CSV format see this [link](/kb/logicbroker/360022057591-Step-6-Testing-Your-Integration?hsLang=en).

#### 👥For Retailers:

To learn more about how to integrate receiving returns from your partners using the CSV format see this link.

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
PRF01 |  **PartnerPO** |  This will be the purchase order number, this will be the main Key to link all your documents. |  **Required**  
BGN02 |  **ReturnNumber** |  Unique Identifier used to identify the Return |  **Required**  
N/A |  **DocumentDate** |  Date of the Return. This field will automatically default with the date the document is created. |  **Required**  
BGN03 |  **ReturnDate** |  Date of the Return. This field will automatically default with the date the document is created. |  **Required**  
N/A |  **ExtendedAttribute.EXAMPLE** |  |  **Optional**  
BLI09 (IN) |  **ReturnLines.ItemIdentifier.PartnerSKU** |  The Item identifier that is internal to the purchaser/merchant. |  **Conditional - if received on an order this value should be returned**  
BLI02 (VN) |  **ReturnLines.ItemIdentifier.SupplierSKU** |  The Item Identifier that is used by the supplier or the person fulfilling the product. |  **Required**  
BLI11 (UP) |  **ReturnLines.ItemIdentifier.UPC** |  Typically the U.P.C Consumer Package code will be provided; however additional standardized codes can be provided here as well. See specific partner instructions for details. |  **Conditional - if received on an order this value should be returned**  
N/A |  **ReturnLines.Price** |  Unit cost that the merchant expects to be billed for each unit fulfilled. |  **Optional**  
BLI03 |  **ReturnLines.Quantity** |  Used to indicate the quantity being returned |  **Required**  
BLI04 |  **ReturnLines.QuantityUOM** |  Unit of Measure for the Quantity being identified for this line. |  **Required**  
BLI:RDR04 (DR) |  **ReturnLines.ReturnReason** |  Free Form Reason for return of the line item. |  **Required**  
BLI:RDR04 (DR) |  **ReturnLines.ReturnReasonCode** |  Code specified by your partner to identify the return reason. Typical codes include:  "1": "Wrong item shipped", "2": "Wrong quantity shipped", "3": "Damaged shipment", "4": "Duplicate shipment", "5": "Arrived late", "6": "Wrong quantity ordered", "7": "Wrong merchandise ordered", "8": "Product quality issue", "9": "Product not as described", "10": "Defective product", "11": "Too small", "12": "Too large", "13": "Not satisfied with sizing", "14": "Not satisfied with color", "15": "Do not want", "16": "Other" "17": "Lower price found", "18": "Customer ordering error" |  **Required**  
N/A |  **ReturnLines.ExtendedAttribute.EXAMPLE** |  |  **N/A**