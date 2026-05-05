---
title: "Inventory Specification"
url: "https://support.logicbroker.com/kb/logicbroker/360022025472-inventory-specification"
category: "Document Standards"
---

March 12, 2026

# Inventory Specification

## 

[🔗Logicbroker_846_EDI_Specs and Samples.zip](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_846_EDI_Specs%20and%20Samples.zip?hsLang=en) (60 KB)  
---  
[🔗inventory template.csv](https://support.logicbroker.com/hubfs/Knowledge%20Base%20Import/inventory%20template.csv?hsLang=en) (1 KB)  
[🔗CSV Sample.csv](https://support.logicbroker.com/hubfs/logicbroker_media/CSV%20Sample.csv?hsLang=en) (2 KB)  
  
Inventory files in Logicbroker are designed to provide quantity and cost updates for all products available to the retailers. Products are typically setup from the retailer side indicating which products are available to be updated, these are identified by the **MerchantSKU**. All feeds received will be matched using the **SupplierSKU** to update the inventory and cost data.

#### ✨Tip:

Not all retailers will have products setup prior to submitting the first inventory update and may require the supplier to create their own products providing the **MerchantSKU** and **SupplierSKU** link. Always check with your retailer partner to verify how products are to be setup.

#### 🗒️Note:

If your a supplier receiving orders, you can update item identifiers on the order using the inventory feed. For example, if you need to receive a UPC or other item identifier we can update the order with information matched by the SupplierSKU from the inventory feed. [Contact us](mailto:sales@logicbroker.com) for more details.

The structure shown below in Field Descriptions follows Logicbroker's standard schema in 2 formats, CSV and EDI. The EDI segments are listed next to each field to indicate what field maps to the standard 846 EDI from the Logicbroker schema.

##### Details and Sample Files

**EDI**

[Download EDI Specs and Samples](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_846_EDI_Specs%20and%20Samples.zip?hsLang=en)

Click the link above to download the standard 846 specification and samples. All fields listed below reflect the model schema for the Logicbroker standard. For example the snippet below would match the EDI field name **REF02 (IO) - Warehouse** in the Field Descriptions below. The value in the parenthesis (IO) will represent the qualifier in the previous element; in this case its REF01.
    
    
    REF*IO*WH1~
    

For EDI fields in a loop like items, will be identified by being separated with a "**:** " for example **LIN:QTY02 (33)** would be represented below. "**LIN:** " indicates the element is under the **LIN** loop. **QTY02** identifies the element value and again "**(33)** " within the parenthesis represents the related qualifier of "**33** " present in **QTY01**. 
    
    
    LIN*1*VN*3C-APORTBARL*UP*018232559661*MG*MFG-5481*ST*ST-2222*SZ*9*VE*BLUE~  
    PID*F*08***PRODUCT DESCRIPTION~  
    CTP*DI*DIS*113.30~  
    REF*ACC*DISC~  
    **QTY*33*14*EA~**

#### 🚚For Suppliers:

To learn more about how to integrate getting inventory using the EDI format see this link.

#### 👥For Retailers:

To learn more about how to integrate sending inventory to your partners using the EDI format see this link.

**CSV**

Click the **CSV Sample** link at the top of the page to download the CSV samples. All fields shown in the table below represent a column in the inventory feed. Each row will contain a new item record, specified by the unique SupplierSKU provided. If there are multiple rows with a duplicate **SupplierSKU** provided, the latest value in the feed will update.

The snippet below shows an example of simple inventory feed, updating only quantity.
    
    
    SupplierSKU,Quantity
    3C-APORTBARL,14

#### 🚚For Suppliers:

To learn more about how to integrate getting inventory using the CSV format see this link.

#### 👥For Retailers:

To learn more about how to integrate sending inventory to your partners using the CSV format see this link.

#### 🗒️Note:

Logicbroker has the ability to create custom specifications for any format and file type. Please [contact us](mailto:sales@logicbroker.com) and attach any samples of your custom format and we can quickly and easily implement it.

##### Field Descriptions

EDI Field | Logicbroker Field | Description | Requirement  
---|---|---|---  
LIN:LIN03 (VN) |  **SupplierSKU** |  SKU for the party that is receiving the purchase order. |  **Mandatory**  
N/A |  **MerchantSKU** |  SKU for the party sending the purchase order. |  **Conditional - Required if setting up products. Used for matching.**  
LIN:LIN05 (UP) |  **UPC** |  UPC Code. |  **Optional**  
LIN: LIN07 (MG) |  **ManufacturerSKU** |  SKU provided by the manufacturer of the product. |  **Optional**  
LIN:QTY02 (33) |  **Quantity** |  Total Quantity available for sale, this would be the total quantity across all warehouses. |  **Mandatory**  
LIN:CTP03 (DIS) |  **Cost** |  Cost sold from the supplier to the merchant. This is the value that will be on the purchase order. |  **Optional**  
N/A |  **MSRP** |  Manufacturer's Suggested Retail Price |  **Optional**  
N/A |  **RetailPrice** |  Price in which the item will be sold to the end customer |  **Optional**  
LIN:PID05 (08) |  **Description** |  Short Description of the product |  **Optional - Used only for Import**  
N/A |  **SupplierDescription** |  Description provided by the supplier. |  **Read Only - Used only for Export**  
N/A |  **MerchantDescription** |  Description provided by the merchant. This is typically done during product setup using the matching file. |  **Read Only - Used only for Export**  
LIN:LIN11 (SZ) |  **Size** |  Size attribute associated with product |  **Optional**  
LIN:LIN13 (VE) |  **Color** |  Color attribute associated with product |  **Optional**  
LIN:LIN09 (ST) |  **Style** |  Unique attribute to identify specific characteristic of the product |  **Optional**  
N/A |  **Weight** |  Total Weight per each Quantity |  **Optional**  
REF02 (IO) |  **Warehouse** |  Code/Identifier indicating location of the Quantity.  |  **Optional**  
LIN:SCH01 (018) |  **NextAvailableQuantity** |  Quantity available given date in "NextAvailableDate" |  **Optional**  
LIN:SCH06 (018) |  **NextAvailableDate** |  Date when next record of inventory will be available |  **Optional**  
LIN:QTY03 |  **UOM** |  Unit of measure for the item getting updated. |  **Optional**  
N/A |  **WarehouseQuantity** |  Total quantity available associated with the Warehouse field. Should match total quantity. |  **Optional**  
LIN:QTY:LS:REF02 (WS) |  **Warehouse2** |  Second Warehouse code/identifer where inventory is located. |  **Optional**  
LIN:QTY:LS:QTY02 (33) |  **Warehouse2Quantity** |  Quantity available at the second warehouse. |  **Optional**  
|  **Warehouse2NextAvailableQuantity** |  Date when next record of inventory will be available for the second warehouse.  |  **Optional**  
LIN:QTY:LS:REF02 (WS) |  **Warehouse3** |  Third Warehouse code/Identifier where inventory is located. |  **Optional**  
LIN:QTY:LS:QTY02 (33) |  **Warehouse3Quantity** |  Quantity available at the third warehouse. |  **Optional**  
|  **Warehouse3NextAvailableQuantity** |  Date when next record of inventory will be available for the third warehouse.  |  **Optional**  
LIN:QTY:LS:REF02 (WS) |  **Warehouse4** |  Fourth Warehouse code/Identifier where inventory is located. |  **Optional**  
LIN:QTY:LS:QTY02 (33) |  **Warehouse4Quantity** |  Quantity available at the fourth warehouse. |  **Optional**  
|  **Warehouse4NextAvailableQuantity** |  Date when next record of inventory will be available for the fourth warehouse.  |  **Optional**  
LIN:QTY:LS:REF02 (WS) |  **Warehouse5** |  Fifth Warehouse code/Identifier where inventory is located. |  **Optional**  
LIN:QTY:LS:QTY02 (33) |  **Warehouse5Quantity** |  Quantity available at the fifth warehouse. |  **Optional**  
|  **Warehouse5NextAvailableQuantity** |  Date when next record of inventory will be available for the fifth warehouse.  |  **Optional**  
LIN:QTY:LS:REF02 (WS) |  **Warehouse6** |  Sixth Warehouse code/Identifier where inventory is located. |  **Optional**  
LIN:QTY:LS:QTY02 (33) |  **Warehouse6Quantity** |  Quantity available at the sixth warehouse. |  **Optional**  
|  **Warehouse6NextAvailableQuantity** |  Date when next record of inventory will be available for the sixth warehouse.  |  **Optional**  
LIN:QTY:LS:REF02 (WS) |  **Warehouse7** |  Seventh warehouse code/Identifier where inventory is located. |  **Optional**  
LIN:QTY:LS:QTY02 (33) |  **Warehouse7Quantity** |  Quantity available at the seventh warehouse. |  **Optional**  
|  **Warehouse7NextAvailableQuantity** |  Date when next record of inventory will be available for the seventh warehouse.  |  **Optional**  
LIN:QTY:LS:REF02 (WS) |  **Warehouse8** |  Eighth Warehouse code/Identifier where inventory is located. |  **Optional**  
LIN:QTY:LS:QTY02 (33) |  **Warehouse8Quantity** |  Quantity available at the eighth warehouse. |  **Optional**  
|  **Warehouse8NextAvailableQuantity** |  Date when next record of inventory will be available for the eighth warehouse.  |  **Optional**  
LIN:QTY:LS:REF02 (WS) |  **Warehouse9** |  Ninth warehouse code/Identifier where inventory is located. |  **Optional**  
LIN:QTY:LS:QTY02 (33) |  **Warehouse9Quantity** |  Quantity available at the ninth warehouse. |  **Optional**  
|  **Warehouse9NextAvailableQuantity** |  Date when next record of inventory will be available for the ninth warehouse.  |  **Optional**  
LIN:QTY:LS:REF02 (WS) |  **Warehouse10** |  Tenth warehouse code/Identifier where inventory is located. |  **Optional**  
LIN:QTY:LS:QTY02 (33) |  **Warehouse10Quantity** |  Quantity available at the tenth warehouse. |  **Optional**  
|  **Warehouse10NextAvailableQuantity** |  Date when next record of inventory will be available for the tenth warehouse.  |  **Optional**  
LIN:REF02 (ACC) |  **Status** |  Status code of the product. Typically to indicate if a product is discontinued or not available. See retailer specifications for what codes are required. |  **Optional**  
LIN:LDT02 |  **Lead Time** |  Time to ship to advertise on retailer's site. |  **Optional**  
N/A |  **LastUpdate** |  Date in which the latest inventory update was provided. |  **Read Only - Used only for Export**