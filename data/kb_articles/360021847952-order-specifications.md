---
title: "Order Specifications"
url: "https://support.logicbroker.com/kb/logicbroker/360021847952-order-specifications"
category: "Document Standards"
---

March 9, 2026

# Order Specifications

## 

🔗 [Logicbroker_Order_CSV_Samples.zip](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Order_CSV_Samples.zip?hsLang=en) (2 KB)  
---  
🔗 [Logicbroker_Order_JSON_Sample.json](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Order_JSON_Sample.json?hsLang=en) (5 KB)  
[🔗Logicbroker_Order_XML_Sample.zip](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Order_XML_Sample.zip?hsLang=en) (4 KB)  
[🔗 Logicbroker 850 EDI Specification.zip](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker%20850%20EDI%20Specification.zip?hsLang=en) (90 KB)  
  
An Order document refers to documents that are intended to be Acknowledged, Shipped and Invoiced. They will contain all necessary data to fulfill and ship items.

The structure shown below in Field Descriptions follows Logicbroker's standard schema across all document formats; this includes JSON, EDI, XML, CSV, and Portal. The EDI segments are listed next to each field to indicate what field maps to the standard 850 EDI from the Logicbroker schema.

#### __ ✨Tip:

If you are integrating via API and need the full model schema see our [API Console.](https://commerceapi.io)

##### Details and Sample Files

**JSON**

[ Download JSON Samples ](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Order_JSON_Sample.json?hsLang=en)

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
    

The value in the field descriptions documentation will show as **ExtendedAttribute.EXAMPLE** and for line items **OrderLine.ExtendedAttribute.EXAMPLE**.

#### __ 🚚For Suppliers:

To learn more about how to integrate receiving orders using the JSON format see this [link](/kb/logicbroker/360022057591-Step-6-Testing-Your-Integration?hsLang=en).

#### __ 👥For Retailers:

To learn more about how to integrate sending orders to your partners using the JSON format see this link.

**XML**

[Download XML Samples + XSD](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Order_XML_Sample.zip?hsLang=en)

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
    

The value in the field descriptions documentation will show as **ExtendedAttribute.EXAMPLE** and for line items **OrderLine.ExtendedAttribute.EXAMPLE**.

####  🚚For Suppliers:

To learn more about how to integrate receiving orders using the XML format see this [link](/kb/logicbroker/360022057591-Step-6-Testing-Your-Integration?hsLang=en).

#### __ 👥For Retailers:

To learn more about how to integrate sending orders to your partners using the XML format see this link.

**EDI**

Click the at the top of the article to download the standard 850 specification and samples. All fields listed below reflect the model schema for the Logicbroker standard XML. For example the snippet below would match the EDI field name **N102 (ST) - ShipToAddress.CompanyName** in the Field Descriptions below. The value in the parenthesis (ST) will represent the qualifier in the previous element; in this case its N101.
    
    
    N1*ST*Merchant Co~
    

For EDI fields in a loop, such as line items, this will be identified by being separated with a " **:** " for example **PO1:PID05 (08)** would be represented below. " **PO1:** " indicates the element is under the **PO1** loop. **PID05** identifies the element value and again " **(08)** " the parenthesis represents the related qualifier of " **08** " present in **PID02**. 
    
    
    PO1*1*5*EA*31.02*TE*VN*49-98760*IN*J07874*UP*123456789012~
    **PID*F*08***Pants~**
    PO1*2*4*EA*12.00*TE*VN*49-98761*IN*J07875*UP*123456789013~
    **PID*F*08***Tee Shirt~**

#### __ 🚚For Suppliers:

To learn more about how to integrate receiving orders using the EDI format see this [link](/kb/logicbroker/360022057591-Step-6-Testing-Your-Integration?hsLang=en).

#### __ 👥For Retailers:

To learn more about how to integrate sending orders to your partners using the EDI format see this link.

**CSV**

[Download CSV Samples](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Order_CSV_Samples.zip?hsLang=en)

Click the link above to download the CSV samples. Note by default if you are retrieving orders from Logicbroker, then by default the format will match the same used in [Import Tracking](https://logicbroker1466521942.zendesk.com/hc/en-us/articles/360020679071-Import-Tracking).

To receive the format as listed below in the Field Descriptions, please contact [support@logicbroker.com](mailto:support@logicbroker.com). All fields listed below reflect the model schema for the Logicbroker standard API format. For example the snippet below would match the field name **ShipToAddress.CompanyName** in the Field Descriptions below.
    
    
    Id,ShipToAddress.CompanyName
    221804,Merchant Co
    

If there is a field that is missing in the structure you can add custom fields as an extended attribute on the header level or item level; see example below. Note when a custom field is added, you will need to notify Logicbroker to ensure it is mapped to your partners.
    
    
    Id,ExtendedAttribute[Name=EXAMPLE].Value
    221804,Portal
    

The value in the field descriptions documentation will show as **ExtendedAttribute.EXAMPLE** and for line items **OrderLine.ExtendedAttributes.EXAMPLE**

#### __ Tip:

When submitting or receiving a **CSV** order, each row will be split out for each line item. If you are submitting an order to Logicbroker for creation, the line items will get consolidated into one order if they share the same **PartnerPO.**

#### __ 🚚For Suppliers:

To learn more about how to integrate receiving orders using the CSV format see this [link](/kb/logicbroker/360022057591-Step-6-Testing-Your-Integration?hsLang=en).

#### __ 👥For Retailers:

To learn more about how to integrate sending orders to your partners using the CSV format see this link.

#### __ 🗒️Note:

Logicbroker has the ability to create custom specifications for any format and file type. Please [contact us](mailto:sales@logicbroker.com) and attach any samples of your custom format and we can quickly and easily implement it.

##### Field Descriptions

EDI Field | Logicbroker Field | Description | Requirement  
---|---|---|---  
N/A |  **Identifier.SourceKey** |  Identifier that will come from the source system; typically this will match the PartnerPO. |  **Read Only**  
N/A |  **Identifier.LogicbrokerKey** |  ID to identify the document in the logicbroker system. Required to save this in your system to prevent duplicates. |  **Read Only**  
N/A |  **Identifier.LinkKey** |  Used to link the document to the original source document. For example, It is best to supply the Order's linkkey when posting a shipment. This will make sure the order shipped quanitites are updated on the original order and all statuses are updated appropriateley. |  **Read Only**  
N/A |  **SenderCompanyId** |  Logicbroker Internal Company ID to specify what company is sending the document. |  **Required**  
N/A |  **ReceiverCompanyId** |  Logicbroker Internal Company ID to specify what company is to receive the document. |  **Required**  
N/A |  **DocumentDate** |  Date the document was created in the logicbroker system. |  **Required**  
CUR02 (ZZ) |  **Currency** |  Currency Code used on the purchase order. |  **Optional**  
REF02 (IT) |  **CustomerNumber** |  End User's customer ID; typically used on the packing slip |  **Optional**  
DTM02 (001) |  **DoNotShipAfter** |  Date in which the PO should be cancelled if the date has been passed before shipment. |  **Optional**  
SAC05 (G821) |  **HandlingAmount** |  Shipping amount to be applied and included in the order total. |  **Optional**  
N9:MSG01 (L1*GFT) |  **Note** |  This section will include gift and packing slip messages. |  **Optional**  
BEG05 |  **OrderDate** |  Date on the Purchase Order |  **Required**  
REF02 (CO) |  **OrderNumber** |  Contains the end customer's order number, this will be used on the packing slip. |  **Required**  
BEG03 |  **PartnerPO** |  This will be the purcahse order number, this will be the main Key to link all your documents. |  **Required**  
BEG02 |  **TypeCode** |  Purchase Order Type Code will indicate what type of PO is being sent. Examples are shown below. SA = Stand Alone RE = Re-Order DS = Drop Ship |  **Optional**  
BEG04 |  **ReleaseNumber** |  Used for replacement orders to not duplicate the fulfillment of the same PO. |  **Optional**  
DTM02 (010) |  **RequestedShipDate** |  Date requested for order to leave the warehouse/shipping location. |  **Optional**  
REF02 (IA) |  **VendorNumber** |  This is the internal vendor number provided to the supplier from the merchant |  **Optional**  
SAC05 (C310) |  **Discount.DiscountAmount** |  Discount amount to be applied and included in the order total. |  **Optional**  
REF02 (PD) |  **Discount.DiscountCode** |  Promotional/Deal Number or Code |  **Optional**  
ITD03 |  **Discount.DiscountPercent** |  Terms Discount Percent to calculate applicable discount amount for timely payment |  **Optional**  
ITD08 |  **PaymentTerm.DiscountAvailable** |  Terms discount amount that will be applied within timely payment. |  **Optional**  
ITD04 |  **PaymentTerm.DiscountDueDate** |  Discount due date when discount will be applied. |  **Optional**  
ITD05 |  **PaymentTerm.DiscountInNumberOfDays** |  Discount days due when discount will be applied. |  **Optional**  
N/A |  **PaymentTerm.EffectiveDate** |  Date when the Payment terms begin. |  **Optional**  
ITD06 |  **PaymentTerm.DueDate** |  Date in which the invoice is due, before additional charges are accrued. |  **Optional**  
ITD07 |  **PaymentTerm.PayInNumberOfDays** |  Number of days in which the invoice is due, before additional charges are accrued. |  **Optional**  
TD503 |  **ShipmentInfo.CarrierCode** |  This will typically be the Standard Carrier Alpha Code (SCAC). |  **Optional**  
TD505 |  **ShipmentInfo.ClassCode** |  The shipping method that will be used to send the merchandise. If you are using Shipment Mappings under **Settings** > **Shipment Options** , [see this article](/kb/logicbroker/360021847232-Step-3-Setup-Ship-Methods#h_64113384791548529471752). |  **Required**  
TD512 |  **ShipmentInfo.ServiceLevelCode** |  Service Level set to ship by the carrier. Check with trading partner to see applicable codes. An example of a few would be: ND = Next Day CG = Ground ON = Overnight SA = Same Day |  **Optional**  
SAC05 (H850) |  **Tax.TaxAmount** |  Tax Amount to be applied and included in the order total. |  **Optional**  
N102 (BT) |  **BillToAddress.CompanyName** |  |  **Required**  
N201 (BT) |  **BillToAddress.FirstName** |  |  **Optional**  
N202 (BT) |  **BillToAddress.LastName** |  |  **Optional**  
N301 (BT) |  **BillToAddress.Address1** |  |  **Required**  
N302 (BT) |  **BillToAddress.Address2** |  |  **Optional**  
N401 (BT) |  **BillToAddress.City** |  |  **Required**  
N402 (BT) |  **BillToAddress.State** |  |  **Required**  
N404 (BT) |  **BillToAddress.Country** |  |  **Optional**  
N403 (BT) |  **BillToAddress.Zip** |  |  **Required**  
N104 (BT*92) |  **BillToAddress.AddressCode** |  Address code that will indicate the location where the address is related to. Typically will be a store or DC number. |  **Optional**  
N1:PER06 (TE) |  **BillToAddress.Phone** |  |  **Optional**  
N1:PER04 (EM) |  **BillToAddress.Email** |  |  **Optional**  
N102 (OB) |  **OrderedByAddress.CompanyName** |  |  **Optional**  
N201 (OB) |  **OrderedByAddress.FirstName** |  |  **Optional**  
N202 (OB) |  **OrderedByAddress.LastName** |  |  **Optional**  
N301 (OB) |  **OrderedByAddress.Address1** |  |  **Optional**  
N302 (OB) |  **OrderedByAddress.Address2** |  |  **Optional**  
N401 (OB) |  **OrderedByAddress.City** |  |  **Optional**  
N402 (OB) |  **OrderedByAddress.State** |  |  **Optional**  
N404 (OB) |  **OrderedByAddress.Country** |  |  **Optional**  
N403 (OB) |  **OrderedByAddress.Zip** |  |  **Optional**  
N104 (OB*92) |  **OrderedByAddress.AddressCode** |  Address code that will indicate the location where the address is related to. Typically will be a store or DC number. |  **Optional**  
N1:PER06 (TE) |  **OrderedByAddress.Phone** |  |  **Optional**  
N1:PER04 (EM) |  **OrderedByAddress.Email** |  |  **Optional**  
N102 (ST) |  **ShipToAddress.CompanyName** |  |  **Required**  
N201 (ST) |  **ShipToAddress.FirstName** |  |  **Optional**  
N202 (ST) |  **ShipToAddress.LastName** |  |  **Optional**  
N301 (ST) |  **ShipToAddress.Address1** |  |  **Required**  
N302 (ST) |  **ShipToAddress.Address2** |  |  **Optional**  
N401 (ST) |  **ShipToAddress.City** |  |  **Required**  
N402 (ST) |  **ShipToAddress.State** |  |  **Required**  
N404 (ST) |  **ShipToAddress.Country** |  |  **Optional**  
N403 (ST) |  **ShipToAddress.Zip** |  |  **Required**  
N104 (ST*92) |  **ShipToAddress.AddressCode** |  Address code that will indicate the location where the address is related to. Typically will be a store or DC number. |  **Optional**  
N1:PER06 (TE) |  **ShipToAddress.Phone** |  |  **Optional**  
N1:PER04 (EM) |  **ShipToAddress.Email** |  |  **Optional**  
REF02 (ST) |  **ExtendedAttribute.StoreNumber** |  Used to identify the store where the order will get shipped for customer pickup. Will also be used to differentiate between D2S and D2C. |  **Optional**  
REF02 (X9) |  **ExtendedAttribute.InternalOrderNumber** |  This is the internal order number within the merchant's system; typically required on the packing slip. |  **Optional**  
REF02 (ZZ) |  **ExtendedAttribute.GiftWrap** |  Will be used to indicate gift wrap. "1" will be used to indicate gift wrapping the entire order. |  **Optional**  
SAC05 (ZZZZ) |  **ExtendedAttribute.MiscCharge** |  Charges to be applied to the PO total; format will be XX.XX |  **Optional**  
SAC05 (N*C310) |  **ExtendedAttribute.CustomerDiscount** |  Discount amount the end customer received. Typically used for drop ship and will be used on the packing slip. Format will be XX.XX |  **Optional**  
SAC05 (N*G821) |  **ExtendedAttribute.CustomerShipping** |  Shipping and Handling amount the end customer paid. Typically used for drop ship and will be used on the packing slip. Format will be XX.XX |  **Optional**  
SAC05 (N*H850) |  **ExtendedAttribute.CustomerTax** |  Tax amount the end customer paid. Typically used for drop ship and will be used on the packing slip. Format will be XX.XX |  **Optional**  
SAC05 (N*ZZZZ) |  **ExtendedAttribute.CustomerMiscCharge** |  Miscellaneous charge amount the end customer paid. This can be gift wrapping charge, special services, etc. Typically used for drop ship and will be used on the packing slip. Format will be XX.XX |  **Optional**  
DTM02 (806) |  **ExtendedAttribute.CustomerOrderDate** |  Will be used to show date when customer placed order; typically used on the packing slip. |  **Optional**  
PO1:PID05 (08) |  **OrderLine.Description** |  Standard short description or name of the product. |  **Optional**  
PO1:CTP03 (RTL) |  **OrderLine.RetailPrice** |  Unit Price to be charged to the customer or end receiver. This will typically be the value on the packing slip. |  **Optional**  
N/A |  **OrderLine.Weight** |  Weight of the product |  **Optional**  
PO1:PO101 |  **OrderLine.LineNumber** |  Purchase order line number. |  **Required**  
N/A |  **OrderLine.Note** |  Specific Notes related to the product. See specific partner for applicable item level messages. |  **Optional**  
PO1:PO104 |  **OrderLine.Price** |  Unit cost that the merchant expects to be billed for each unit fulfilled. |  **Optional**  
PO1:PO105 |  **OrderLine.PriceCode** |  Used to indicate the price level for the product. See specific partner details for applicable codes. |  **Optional**  
PO1:PO102 |  **OrderLine.Quantity** |  Contains the quantity of items to be fulfilled. |  **Required**  
PO1:PO103 |  **OrderLine.QuantityUOM** |  Unit of Measure for the quantity ordered. See partner's details for specifics. |  **Required**  
N/A |  **OrderLine.ItemIdentifier.ISBN** |  International Standard Book Number |  **Optional**  
N/A |  **OrderLine.ItemIdentifier.ManufacturerSKU** |  Manufacturer's ID for the product. |  **Optional**  
PO1:PO109 (IN) |  **OrderLine.ItemIdentifier.PartnerSKU** |  The Item identifier that is internal to the purchaser/merchant. |  **Optional**  
PO1:PO107 (VN) |  **OrderLine.ItemIdentifier.SupplierSKU** |  The Item Identifier that is used by the supplier or the person fulfilling the product. |  **Required**  
PO1:PO111 (UP) |  **OrderLine.ItemIdentifier.UPC** |  Typically the U.P.C Consumer Package code will be provided; however additional standardized codes can be provided here as well. See specific partner instructions for details. |  **Optional**  
PO1:SAC05 (C310) |  **OrderLine.Discount.DiscountAmount** |  Discount amount applied to the corresponding item. |  **Optional**  
PO1:TD503 |  **OrderLine.ShipmentInfo.CarrierCode** |  Used for specific shipping instructions on the line item level. This will typically be the Standard Carrier Alpha Code (SCAC). |  **Optional**  
PO1:TD505 |  **OrderLine.ShipmentInfo.ClassCode** |  Item level shipping method that will be used to send the merchandise. This is a free form field and can include UPS Ground, or Overnight, etc. |  **Optional**  
PO1:PO406 |  **OrderLine.ShipmentInfo.Weight** |  Total weight of the package or carton. |  **Optional**  
PO1:PO407 |  **OrderLine.ShipmentInfo.WeightUnit** |  Weight Unit of Measure for the package or carton. |  **Optional**  
PO1:SAC05 (H850) |  **OrderLine.Tax.TaxAmount** |  Item Level Tax amount |  **Optional**  
PO1:PID05 (35) |  **OrderLine.ExtendedAttribute.Color** |  Color code used to identify specific product attribute. Can also include color description; see specific partner for details. |  **Optional**  
PO1:N9:MSG01 (L1*GFT) |  **OrderLine.ExtendedAttribute.Gift Message** |  Item Level Gift Message |  **Optional**  
PO1:MSG01 |  **OrderLine.ExtendedAttribute.Item Level Message** |  Item Level message, to specify additional details for the product. This can include customizations or other instructions. |  **Optional**  
PO1:PID05 (SIZ) |  **OrderLine.ExtendedAttribute.Size** |  Size identifier for the product. |  **Optional**  
PO1:REF02 (ZZ) |  **OrderLine.ExtendedAttribute.GiftWrap** |  Will be used to indicate gift wrap. "1" will be used to indicate gift wrapping this specific item. |  **Optional**  
PO1:SAC05 (ZZZZ) |  **OrderLine.ExtendedAttribute.MiscCharge** |  Item level charges to be applied to the PO total; format will be XX.XX |  **Optional**  
PO1:SAC05 (N*C310) |  **OrderLine.ExtendedAttribute.CustomerDiscount** |  Item level discount amount the end customer received. Typically used for drop ship and will be used on the packing slip. Format will be XX.XX |  **Optional**  
PO1:SAC05 (N*G821) |  **OrderLine.ExtendedAttribute.CustomerShipping** |  Item level shipping and Handling amount the end customer paid. Typically used for drop ship and will be used on the packing slip. Format will be XX.XX |  **Optional**  
PO1:SAC05 (N*H850) |  **OrderLine.ExtendedAttribute.CustomerTax** |  Tax amount the end customer paid. Typically used for drop ship and will be used on the packing slip. Format will be XX.XX |  **Optional**  
PO1:SAC05 (N*ZZZZ) |  **OrderLine.ExtendedAttribute.CustomerMiscCharge** |  Miscellaneous charge amount the end customer paid. This can be gift wrapping charge, special services, etc. Typically used for drop ship and will be used on the packing slip. Format will be XX.XX |  **Optional**  
PO1:N9:MSG01 (L1*ZZZ) |  **OrderLine.ExtendedAttribute.SpecialInstructions** |  This would include instruction on packing or shipping this specific item. |  **Optional**  
PO1:PID05 (ZZ) |  **OrderLine.ExtendedAttribute.MiscItemIdentifier** |  This would be an item identifier that does not fit in the standard SupplierSKU, PartnerSKU, or UPC. You would need to refer to the specific trading partner on the usage. |  **Optional**  
PO1.MAN (01, 02) |  **01: MAN02_[Qualifier]** **02: Value(s)** |  Container code. Logicbroker will map the MAN qualifier to MAN02_[Qualifier] with the value(s) listed in the Value field. |  **Optional**  
LIN.MOA (203, 1) |  **203: OrderLine.Price**(if not present on PRI segment) **203: OrderLine.ExtendedAttribute.MOA_203** **1: OrderLine.ExtendedAttribute.MOA_1** |  Monetary Amount. If Price is not populated by a PRI segment, Logicbroker will map it to Price. All MOA segments will be mapped to KVPs on the order. |  **Optional**