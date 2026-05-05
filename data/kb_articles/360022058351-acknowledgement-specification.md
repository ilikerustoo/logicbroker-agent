---
title: "Acknowledgement Specification"
url: "https://support.logicbroker.com/kb/logicbroker/360022058351-acknowledgement-specification"
category: "Document Standards"
---

March 10, 2026

# Acknowledgement Specification

## 

[🔗Logicbroker_Acknowledgement_CSV_Samples.zip](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Acknowledgement_CSV_Samples.zip?hsLang=en) (1 KB)  
---  
[](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Acknowledgement_JSON_Sample.json?hsLang=en)[🔗](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Acknowledgement_CSV_Samples.zip?hsLang=en)[Logicbroker_Acknowledgement_JSON_Sample.json](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Acknowledgement_JSON_Sample.json?hsLang=en) (2 KB)  
[](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Acknowledgement_XML_Standard.zip?hsLang=en)[🔗](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Acknowledgement_CSV_Samples.zip?hsLang=en)[Logicbroker_Acknowledgement_XML_Standard.zip](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Acknowledgement_XML_Standard.zip?hsLang=en) (3 KB)  
[](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker%20855%20EDI%20Sample%20and%20Specifications.zip?hsLang=en)[🔗](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Acknowledgement_CSV_Samples.zip?hsLang=en)[Logicbroker 855 EDI Sample and Specifications.zip](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker%20855%20EDI%20Sample%20and%20Specifications.zip?hsLang=en) (50 KB)  
  
In Logicbroker the Acknowledgment's purpose is to accept, backorder and cancel items from an order received. Accepting items is typically required to indicate that you are ready to fulfill and ship an order. Backordering an item indicates that you will not ship the item until it is back in stock, this is usually beyond the standard 24 hours shipping window. Last cancelling items indicates that the item will not be fulfilled. All acknowledgements must match the **PartnerPO** from a previous order otherwise the document will not process.

#### ✨ Tip:

Not all retailers and channels accept the **Acknowledgement** document and some only use it for accepting, cancelling, backordering, or any combination of the 3. Some may not allow for partial line cancellations or backorders, therefore follow the test cases when onboarding to verify what options are available. Also, if an acknowledgement is received with incorrect or non-compliant data the document will go to a **Failed** status and no data transmitted to the channel.

When receiving an acknowledgement against and order, it will effect the status of that order. If all quantities on the order are cancelled, the status of the order will automatically update to **Cancelled** (1100). It is important to note that all acknowledgments must have the **PartnerPO** and **SupplierSKU** match the original order otherwise the document will be non-compliant and fail to process.

#### ✨ Tip:

Sending or Receiving an acknowledgement with accepted quantities can be used to update the original order status as well. Typically this will move your order from **Ready to Acknowledge** (150) to **Ready to Ship** (500).

#### 🗒️Note:

For Logicbroker customers, if you will be accepting all orders received, we can implement auto-acknowledging for all orders. This will auto create and acknowledgement for every order received for your partners. For more details [contact us](mailto:sales@logicbroker.com).

The structure shown below in Field Descriptions follows Logicbroker's standard schema across all document formats; this includes JSON, EDI, XML, CSV, and Portal. The EDI segments are listed next to each field to indicate what field maps to the standard 855 EDI from the Logicbroker schema.

#### ✨ Tip:

If you are integrating via API and need the full model schema see our [API Console.](https://commerceapi.io)

##### Details and Sample Files

**JSON**

[ Download JSON Samples ](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Acknowledgement_JSON_Sample.json?hsLang=en)

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
    

The value in the field descriptions documentation will show as **ExtendedAttribute.EXAMPLE** and for line items **AckLines.ExtendedAttribute.EXAMPLE**.

#### __ For Suppliers:

To learn more about how to integrate sending acknowledgements using the JSON format see this [link](/kb/logicbroker//360022057591-Step-6-Testing-Your-Integration?hsLang=en).

#### __ For Retailers:

To learn more about how to integrate receiving acknowledgements from your partners using the JSON format see this link.

**XML**

[Download XML Samples + XSD](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Acknowledgement_XML_Standard.zip?hsLang=en)

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
    

The value in the field descriptions documentation will show as **ExtendedAttribute.EXAMPLE** and for line items **AckLines.ExtendedAttribute.EXAMPLE**.

#### __ For Suppliers:

To learn more about how to integrate sending acknowledgements using the XML format see this [link](/kb/logicbroker/360022057591-Step-6-Testing-Your-Integration?hsLang=en).

#### __ For Retailers:

To learn more about how to integrate receiving acknowledgements from your partners using the XML format see this link.

**EDI**

[Download EDI Specs and Samples](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker%20855%20EDI%20Sample%20and%20Specifications.zip?hsLang=en)

Click the link above to download the standard 855 specification and samples. All fields listed below reflect the model schema for the Logicbroker standard 855. For example the snippet below would match the EDI field name **N102 (ST) - ShipToAddress.CompanyName** in the Field Descriptions below. The value in the parenthesis (ST) will represent the qualifier in the previous element; in this case its N101.
    
    
    N1*ST*Merchant Co~
    

For EDI fields in a loop, such as line items, they will be identified by being separated with a "**:** " for example **PO1:ACK02 (IA)** would be represented below. "**PO1:** " indicates the element is under the **PO1** loop. **ACK02** identifies the element value and the parenthesis "**(IA)** " represents the related qualifier of "**IA** " present in **ACK01**.

#### ✨ Tip:

The ACK segment can be used 3 times under the PO1 loop to indicate accepted (IA), cancelled (IR), and backordered (IB) quantities. 
    
    
    PO1*1*90*EA***VN*V-123123*IN*1234567*UP*0123456789012~  
    **ACK*IA*88*EA~**  
    **ACK*IB*1*EA~**  
    **ACK*IR*1*EA~**  
     DTM*068*20160728~
    

#### __ For Suppliers:

To learn more about how to integrate sending acknowledgements using the EDI format see this [link](/kb/logicbroker//360022057591-Step-6-Testing-Your-Integration?hsLang=en).

#### __ For Retailers:

To learn more about how to integrate receiving acknowledgements from your partners using the EDI format see this link.

**CSV**

[Download CSV Samples](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Acknowledgement_CSV_Samples.zip?hsLang=en)

Click the link above to download the CSV samples. Note by default if you are retrieving acknowledgements from Logicbroker's SFTP/FTP a simplified version is identified with the "**EXPORT** " annotation on the file name.

To receive the format as listed below in the Field Descriptions, please contact [support@logicbroker.com](mailto:support@logicbroker.com). All fields listed below reflect the model schema for the Logicbroker standard CSV format. For example the snippet below would match the field name **ShipToAddress.CompanyName** in the Field Descriptions below.
    
    
    Id,ShipToAddress.CompanyName
    221804,Merchant Co
    

If there is a field that is missing in the structure you can add custom fields as an extended attribute on the header level or item level; see example below. Note when a custom field is added, you will need to notify Logicbroker to ensure it is mapped to your partners.
    
    
    Id,ExtendedAttribute[Name=EXAMPLE].Value
    221804,Portal
    

The value in the field descriptions documentation will show as **ExtendedAttribute.EXAMPLE** and for line items **AckLines.ExtendedAttribute.EXAMPLE**

#### ✨ Tip:

When submitting or receiving a **CSV** acknowledgement, each row will be split out for each line item. If you are submitting an acknowledgement to Logicbroker for creation, the line items will get consolidated into one acknowledgement if they share the same **AcknowledgementNumber** and **PartnerPO.**

#### __ For Suppliers:

To learn more about how to integrate sending acknowledgements using the CSV format see this [link](/kb/logicbroker//360022057591-Step-6-Testing-Your-Integration?hsLang=en).

#### __ For Retailers:

To learn more about how to integrate receiving acknowledgements from your partners using the CSV format see this link.

#### 🗒️Note:

Logicbroker has the ability to create custom specifications for any format and file type. Please [contact us](mailto:sales@logicbroker.com) and attach any samples of your custom format and we can quickly and easily implement it.

##### Field Descriptions

EDI Field | Logicbroker Field | Description | Requirement  
---|---|---|---  
N/A |  **Identifier.SourceKey** |  Identifier that will come from the source system; typically this will match the PartnerPO. |  **Read Only**  
N/A |  **Identifier.LogicbrokerKey** |  ID to identify the document in the logicbroker system. |  **Read Only**  
N/A |  **Identifier.LinkKey** |  Used to link the document to the original source document. For example, It is best to supply the Order's linkkey when posting a shipment. This will make sure the order shipped quanitites are updated on the original order and all statuses are updated appropriateley. |  **Read Only**  
N/A |  **SenderCompanyId** |  Logicbroker Internal Company ID to specify what company is sending the document. |  **Required**  
N/A |  **ReceiverCompanyId** |  Logicbroker Internal Company ID to specify what company is to receive the document. |  **Required**  
BAK02 |  **Type** |  Indicates how the acknowledgement will be treated. 0 = AcknowledgeWithChange 1 = Acknowledge 2 = Reject |  **Optional - if not sent the type of acknowledgement will be determined by the Quantites accepted, cancelled, or backordered on the line level.**  
N/A |  **OrderNumber** |  Contains the end customer's order number, this will be used on the packing slip. |  **Will pull from Order**  
BAK03 |  **PartnerPO** |  This will be the purchase order number, this will be the main Key to link all your documents. This should match the order. |  **Required**  
BAK09 |  **OrderDate** |  Date on the Purchase Order |  **Optional - will be pulled from original order if not provided**  
BAK08 |  **AcknowledgementNumber** |  Unique Identifier used to identify the acknowledgment |  **Required**  
PO1:ACK:DTM02 (068) or PO1:ACK05 (068) |  **ScheduledShipDate** |  Used to identify the date the items listed on the acknowledgement will ship. |  **Required**  
BAK04 |  **DocumentDate** |  Date of the Acknoweldgement. This field will automatically default with the date the document is created. |  **Read Only**  
N/A |  **ExtendedAttribute.EXAMPLE** |  |  **Optional**  
PO1:PO109 (IN) |  **AckLines.ItemIdentifier.PartnerSKU** |  The Item identifier that is internal to the purchaser/merchant. |  **Conditional - if received on an order this value should be returned**  
PO1:PO107 (VN) |  **AckLines.ItemIdentifier.SupplierSKU** |  The Item Identifier that is used by the supplier or the person fulfilling the product. This will always contain a value. |  **Required**  
PO1:PO111 (UP) |  **AckLines.ItemIdentifier.UPC** |  Typically the U.P.C Consumer Package code will be provided; however additional standardized codes can be provided here as well. See specific partner instructions for details. |  **Conditional - if received on an order this value should be returned**  
PO1:PO104 |  **AckLines.Price** |  Unit cost that the merchant expects to be billed for each unit fulfilled. |  **Optional - only necessary to be provided if there is a change from the order**  
PO1:PO105 |  **AckLines.PriceCode** |  Used to indicate the price level for the product. See specific partner details for applicable codes. |  **Optional - only necessary to be provided if there is a change from the order**  
PO1:PO101 |  **AckLines.LineNumber** |  Purchase order line number. |  **Conditional - if received on an order this value should be returned**  
PO1:ACK02 (IA) |  **AckLines.Quantity** |  Used to list the quantity being acknowledged for this product. The acknowledgement type will be determined by the what is supplied in the "Type" and "ChangeReason" fields. |  **Conditional - Required if Accepting items**  
PO1:ACK02 (IR) |  **AckLines.QuantityCancelled** |  If this value is provided, Qty will get automatically updated and the change reason will get updated appropriately. |  **Conditional - Required if Cancelling items**  
PO1:ACK02 (IB) |  **AckLines.QuantityBackordered** |  If this value is provided, Qty will get automatically updated and the change reason will get updated appropriately. |  **Conditional - Required if Backordering items**  
PO1:ACK03 |  **AckLines.QuantityUOM** |  Unit of Measure for the Quantity being identified for this line. |  **Optional - only necessary to be provided if there is a change from the order**  
PO1:N902 (TD) |  **AckLines.ChangeReason** |  Free Form Reason for cancellation, or acceptance of line item. For certain partners this may require a specific code; the standard codes are listed below. Administrative request  
Bad address  
Cancelled at retailer's request  
Cannot fulfill in time  
Cannot ship to PO box.  
Cannot ship using provided ship method  
Customer changed mind  
Discontinued item  
Duplicate order  
Fraud detected  
Info missing on purchase order  
Invalid SKU  
Invalid item cost  
Invalid ship method  
Item recall  
Other  
Out of stock |  **Optional**