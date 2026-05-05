---
title: "Shipment Specifications"
url: "https://support.logicbroker.com/kb/logicbroker/360022058371-shipment-specifications"
category: "Document Standards"
---

March 10, 2026

# Shipment Specifications

## 

[🔗Logicbroker_Shipment_CSV_Samples.zip](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Shipment_CSV_Samples.zip?hsLang=en) (2 KB)  
---  
[🔗Logicbroker_Shipment_XML_Sample and Schema.zip](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Shipment_XML_Sample%20and%20Schema.zip?hsLang=en) (6 KB)  
[🔗Logicbroker_Shipment_JSON_Samples.zip](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Shipment_JSON_Samples.zip?hsLang=en) (3 KB)  
[🔗Logicbroker_856_EDI_Specs and Samples (1).zip](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_856_EDI_Specs%20and%20Samples%20\(1\).zip?hsLang=en) (90 KB)  
  
In Logicbroker the shipment's purpose is to provide all information related to shipping ordered items. This will include quantities shipped, tracking information, container codes (GS1-128 if required) and carrier information.

#### ✨Tip:

It is important to understand what kind of shipments are being transmitted. Freight shipments sent to a distribution center or warehouses are typically treated differently then a shipment to a residential property. This may include providing GS1-128 labels on all packages or sending pallet information. If you have questions for a specific partner and requirements please [contact support](mailto:support@logicbroker.com).

Not all shipments require a **GS1-128** code and label, which will be supplied in the **ShipmentLine.ShipmentInfo.ContainerCode** field. In most cases the **ShipmentLine.ShipmentInfo.TrackingNumber** will be used to identify each unique package/carton.

#### 🗒️Note:

If you need to implement a **GS1-128** label and code we can generate both the code and label automatically verifying full compliance across all your partners. For more info [contact us](mailto:sales@logicbroker.com).

When receiving as shipment against your order, it will effect the status of that order. If all quantities on the order are shipped the status of the order will automatically update to **Ready to Invoice**(600) or **Complete** (1000) if no invoice is required. It is important that the **PartnerPO** and all **SupplierSKU** data on the shipment matches the order otherwise the shipment will be non-compliant and will not transmit. 

#### 🗒️Note:

If you need to cancel items from an order and do not want to implement an Acknowledgement document type integration, you can use the shipment. [Contact us](mailto:sales@logicbroker.com) for more details.

The structure shown below in Field Descriptions follows Logicbroker's standard schema across all document formats; this includes JSON, EDI, XML, CSV, and Portal. The EDI segments are listed next to each field to indicate what field maps to the standard 856 EDI from the Logicbroker schema.

#### ✨Tip:

If you are integrating via API and need the full model schema see our [API Console.](https://commerceapi.io)

**Consolidated Shipments**

Logicbroker supports suppliers sending in consolidated shipments (1 shipment for multiple orders). To send in a consolidated 856, you will need to indicate multiple order loopes within the document. Logicbroker will create individual 856s based on that information and send the shipments to retailers as individual shipments per order. For any retailer that has test cases, suppliers can test sending consolidated shipments using those test cases. 

##### Details and Sample Files

**JSON**

[ Download JSON Samples ](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Shipment_JSON_Samples.zip?hsLang=en)

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
    

The value in the field descriptions documentation will show as **ExtendedAttribute.EXAMPLE** and for line items **ShipmentLine.ExtendedAttribute.EXAMPLE**.

All shipments must include package/carton information. This data is provided in the **ShipmentInfos** array. There is a header level **ShipmentInfos** which will be used to define pallets and there are item level **ShipmentLine.ShipmentInfos** to indicate the quantity shipped in each package/carton; this is always required. An example of the different hierarchies are shown below:

##### Standard (No Pallet)

Notice the quantity shipped will always be entered under the **ShipmentLine.ShipmentInfo** in **Qty**. This is to show how much of each quantity is shipped in each package/container. All carrier and tracking information is also required and provided here. The **Quantity** field is not required and will auto-populate with the total quantity across multiple containers.
    
    
    {
      "ShipmentLines": [
        {
          "ItemIdentifier": {
            "SupplierSKU": "V-123123"
          },
          "ShipmentInfos": [
            {
              "DateShipped": "2019-01-01T12:00:00",
              "CarrierCode": "FEDG",
              "ClassCode": "FDEG_GD",
              "ServiceLevelCode": "string",
              "TrackingNumber": "TRK11111",
              "ContainerCode": "00086275400000051594",
              **"Qty" : 15,**
              "ContainerType": "CTN",
              "Height": 1.0,
              "Width": 2.0,
              "Length": 3.0,
              "DimensionUnit": "IN",
              "Weight": 0.0,
              "WeightUnit": "LB"
            },
          "ShipmentInfos": [
            {
              "DateShipped": "2019-01-01T12:00:00",
              "CarrierCode": "FEDG",
              "ClassCode": "FDEG_GD",
              "ServiceLevelCode": "string",
              "TrackingNumber": "TRK22222",
              "ContainerCode": "00086275400000051595",
              **"Qty" : 5,**
              "ContainerType": "CTN",
              "Height": 1.0,
              "Width": 2.0,
              "Length": 3.0,
              "DimensionUnit": "IN",
              "Weight": 0.0,
              "WeightUnit": "LB"
            },
          ],
          **"Quantity" : 20,**
          "QuantityUOM": "EA",
          "LineNumber": "1"
        }
      ]
    }
    

##### With Pallet

In the case of sending pallet info and to indicate which cartons will be shipped on each pallet, the **ShipmentInfo.ContainerCode** on the header level will match the **ShipmentLine.ShipmentInfo.ShipmentContainerParentCode**. The container code will typically be a GS1-128 code.
    
    
    {
      "ShipmentInfos": [
        {
          "DateShipped": "0001-01-01T00:00:00",
          **"ContainerCode" : "00086275400000051600",**
          "ContainerType": "PLT",
          "Height": 4.0,
          "Width": 4.0,
          "Length": 5.0,
          "DimensionUnit": "IN",
          "Weight": 0.0,
          "WeightUnit": "LB"
        }
      ],
      "ShipmentLines": [
        {
          "ItemIdentifier": {
            "SupplierSKU": "V-123123"
          },
          "ShipmentInfos": [
            {
              "DateShipped": "2019-01-01T12:00:00",
              "CarrierCode": "FEDG",
              "ClassCode": "FDEG_GD",
              "ServiceLevelCode": "string",
              "TrackingNumber": "TRK11111",
              "ContainerCode": "00086275400000051594",
              "Qty": 15,
              "ContainerType": "CTN",
              **"ShipmentContainerParentCode" : "00086275400000051600",**
              "Height": 1.0,
              "Width": 2.0,
              "Length": 3.0,
              "DimensionUnit": "IN",
              "Weight": 0.0,
              "WeightUnit": "LB"
            },
          "ShipmentInfos": [
            {
              "DateShipped": "2019-01-01T12:00:00",
              "CarrierCode": "FEDG",
              "ClassCode": "FDEG_GD",
              "ServiceLevelCode": "string",
              "TrackingNumber": "TRK22222",
              "ContainerCode": "00086275400000051595",
              **"ShipmentContainerParentCode" : "00086275400000051600",**
              "Qty": 5,
              "ContainerType": "CTN",
              "Height": 1.0,
              "Width": 2.0,
              "Length": 3.0,
              "DimensionUnit": "IN",
              "Weight": 0.0,
              "WeightUnit": "LB"
            },
          ],
          "Quantity": 20,
          "QuantityUOM": "EA",
          "LineNumber": "1"
        }
      ]
    }

#### 🚚 For Suppliers:

To learn more about how to integrate sending shipments using the JSON format see this [link](/kb/logicbroker/360022057591-Step-6-Testing-Your-Integration?hsLang=en).

#### 👥 For Retailers:

To learn more about how to integrate receiving shipments from your partners using the JSON format see this link.

**XML**

[Download XML Samples + XSD](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Shipment_XML_Sample%20and%20Schema.zip?hsLang=en)

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
    

The value in the field descriptions documentation will show as **ExtendedAttribute.EXAMPLE** and for line items **ShipmentLine.ExtendedAttribute.EXAMPLE**.

All shipments must include package/carton information. This data is provided in the **ShipmentInfos** array. There is a header level **ShipmentInfos** which will be used to define pallets and there are item level **ShipmentLine.ShipmentInfos** to indicate the quantity shipped in each package/carton; this is always required. An example of the different hierarchies are shown below:

##### Standard (No Pallet)

Notice the quantity shipped will always be entered under the **ShipmentLine.ShipmentInfo** in **Qty**. This is to show how much of each quantity is shipped in each package/container. All carrier and tracking information is also required and provided here. The **Quantity** field is not required and will auto-populate with the total quantity across multiple containers.
    
    
    <Shipment xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
      <ShipmentLines>
        <ShipmentLine>
          <ItemIdentifier>
            <SupplierSKU>V-123123</SupplierSKU>
          </ItemIdentifier>
          <ShipmentInfos>
            <ShipmentInfo>
              <DateShipped>2019-01-01T12:00:00</DateShipped>
              <CarrierCode>FEDG1</CarrierCode>
              <ClassCode>FDEG_GD</ClassCode>
              <ServiceLevelCode>string</ServiceLevelCode>
              <TrackingNumber>TRK11111</TrackingNumber>
              <ContainerCode>00086275400000051594</ContainerCode>
              **< Qty>15</Qty>**
              <ContainerType>CTN</ContainerType>
              <Height>1</Height>
              <Width>2</Width>
              <Length>3</Length>
              <DimensionUnit>IN</DimensionUnit>
              <Weight>0</Weight>
              <WeightUnit>LB</WeightUnit>
            </ShipmentInfo>
            <ShipmentInfo>
              <DateShipped>2019-01-01T12:00:00</DateShipped>
              <CarrierCode>FEDG1</CarrierCode>
              <ClassCode>FDEG_GD</ClassCode>
              <ServiceLevelCode>string</ServiceLevelCode>
              <TrackingNumber>TRK22222</TrackingNumber>
              <ContainerCode>00086275400000051595</ContainerCode>
              **< Qty>5</Qty>**
              <ContainerType>CTN</ContainerType>
              <Height>1</Height>
              <Width>2</Width>
              <Length>3</Length>
              <DimensionUnit>IN</DimensionUnit>
              <Weight>0</Weight>
              <WeightUnit>LB</WeightUnit>
            </ShipmentInfo>
          </ShipmentInfos>
          **< Quantity>20</Quantity>**
          <QuantityUOM>EA</QuantityUOM>
          <LineNumber>1</LineNumber>
        </ShipmentLine>
      </ShipmentLines>
    </Shipment>

##### With Pallet

In the case of sending pallet info and to indicate which cartons will be shipped on each pallet, the **ShipmentInfo.ContainerCode** on the header level will match the **ShipmentLine.ShipmentInfo.ShipmentContainerParentCode**. The container code will typically be a GS1-128 code.
    
    
    <Shipment xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
      <ShipmentInfos>
        <ShipmentInfo>
          <DateShipped>0001-01-01T00:00:00</DateShipped>
          **< ContainerCode>00086275400000051600</ContainerCode>**
          <ContainerType>PLT</ContainerType>
          <Height>4</Height>
          <Width>4</Width>
          <Length>5</Length>
          <DimensionUnit>IN</DimensionUnit>
          <Weight>0</Weight>
          <WeightUnit>LB</WeightUnit>
        </ShipmentInfo>
      </ShipmentInfos>
      <ShipmentLines>
        <ShipmentLine>
          <ItemIdentifier>
            <SupplierSKU>V-123123</SupplierSKU>
          </ItemIdentifier>
          <ShipmentInfos>
            <ShipmentInfo>
              <DateShipped>2019-01-01T12:00:00</DateShipped>
              <CarrierCode>FEDG1</CarrierCode>
              <ClassCode>FDEG_GD</ClassCode>
              <ServiceLevelCode>string</ServiceLevelCode>
              <TrackingNumber>TRK11111</TrackingNumber>
              <ContainerCode>00086275400000051594</ContainerCode>
              <Qty>15</Qty>
              <ContainerType>CTN</ContainerType>
    ** <ShipmentContainerParentCode>00086275400000051600</ShipmentContainerParentCode>
    **          <Height>1</Height>
              <Width>2</Width>
              <Length>3</Length>
              <DimensionUnit>IN</DimensionUnit>
              <Weight>0</Weight>
              <WeightUnit>LB</WeightUnit>
            </ShipmentInfo>
            <ShipmentInfo>
              <DateShipped>2019-01-01T12:00:00</DateShipped>
              <CarrierCode>FEDG1</CarrierCode>
              <ClassCode>FDEG_GD</ClassCode>
              <ServiceLevelCode>string</ServiceLevelCode>
              <TrackingNumber>TRK22222</TrackingNumber>
              <ContainerCode>00086275400000051595</ContainerCode>
              <Qty>5</Qty>
              <ContainerType>CTN</ContainerType>
    ** <ShipmentContainerParentCode>00086275400000051600</ShipmentContainerParentCode>
    **          <Height>1</Height>
              <Width>2</Width>
              <Length>3</Length>
              <DimensionUnit>IN</DimensionUnit>
              <Weight>0</Weight>
              <WeightUnit>LB</WeightUnit>
            </ShipmentInfo>
          </ShipmentInfos>
          <Quantity>20</Quantity>
          <QuantityUOM>EA</QuantityUOM>
          <LineNumber>1</LineNumber>
        </ShipmentLine>
      </ShipmentLines>
    </Shipment>

#### 🚚 For Suppliers:

To learn more about how to integrate sending shipments using the XML format see this [link](/kb/logicbroker/360022057591-Step-6-Testing-Your-Integration?hsLang=en).

#### 👥 For Retailers:

To learn more about how to integrate receiving shipments from your partners using the XML format see this link.

**EDI**

Download EDI Specs and Samples

Click the link above to download the standard 856 specification and samples. All fields listed below reflect the model schema for the Logicbroker standard 856. For example the snippet below would match the EDI field name **N102 (ST) - ShipToAddress.CompanyName** in the Field Descriptions below. The value in the parenthesis (ST) will represent the qualifier in the previous element; in this case its N101.
    
    
    N1*ST*Merchant Co~
    

For EDI fields in a loop, such as line items, they will be identified by being separated with a "**:** " for example **HL*I:LIN103 (VN)** would be represented below. "**HL*I:** " indicates the element is under the **HL item** loop. **LIN02** identifies the element value and again the parenthesis "**(VN)** " represents the related qualifier of "**VN** " present in **LIN02**.
    
    
    **HL*5*4*I~**  
    **LIN*1*VN*49-98760** *IN*J07874*UP*123456789012~  
    SN1**298*EA~
    

All shipments must include package/carton information. There is a header level **HL*T loop** which will be used to define pallet information and the pack level **HL*P loop** will contain item and quantity shipped info per each package/carton; this is always required. An example of the different hierarchies is shown below:

##### Standard (No Pallet)

Notice the quantity shipped will always be entered under the **SN1** segment. This is to show how much of each quantity is shipped in each package/container. The **HL02** loop will indicate what container the items belong to, this is the parent Id. The **MAN*CP** will contain tracking information and **MAN*GM** will normally be the GS1-128 code if required.

In the example shown this is a SOPI (Shipment, Order, Pack, Item) structure and shows one line item getting shipped in 2 different packages/cartons.
    
    
    **HL*3*2*P~**  
     PO4**********4*3*2*IN~  
    TD1*CTN*1****G*20*LB~  
    MAN*CP*564564654654~  
    MAN*GM*081034001000008795~  
    **HL*4*3*I~**  
     LIN*1*VN*49-98760*IN*J07874*UP*123456789012~  
    **SN1**298*EA~**  
    **HL*5*2*P~**  
     PO4**********4*3*2*IN~  
    TD1*CTN*1****G*20*LB~  
    MAN*CP*854545488888~  
    MAN*GM*081034001000008818~  
    **HL*6*5*I~**  
     LIN*1*VN*49-98760*IN*J07874*UP*123456789012~  
    **SN1**1*EA~**  
    

##### With Pallet

In the example shown this is a SOTPI (Shipment, Order, Tare, Pack, Item) structure and shows shipping one pallet with one line item getting shipped in 2 different packages/cartons under that pallet. The **HL02** loop will show the parent Id and will indicate what pallet and container the items belong to. 
    
    
    **HL*3*2*T~**  
     TD1*PLT*1****G*400*LB*1000*IN~  
    REF*ZH*1Z324323~  
    MAN*GM*181034001000008808~  
    **HL*4*3*P~**  
     PO4**********4*3*2*IN~  
    TD1*CTN*1****G*20*LB~  
    MAN*CP*564564654654~  
    MAN*GM*081034001000008795~  
    **HL*5*4*I~**  
     LIN*3*VN*49-98760*IN*J07874*UP*123456789012~  
    SN1**298*EA~  
    **HL*6*3*P~**  
     PO4**********4*3*2*IN~  
    TD1*CTN*1****G*20*LB~  
    MAN*CP*854545488888~  
    MAN*GM*081034001000008818~  
    **HL*7*6*I~**  
     LIN*1*VN*49-98760*IN*J07874*UP*123456789012~  
    SN1**1*EA~

#### 🚚 For Suppliers:

To learn more about how to integrate sending shipments using the EDI format see this [link](/kb/logicbroker/360022057591-Step-6-Testing-Your-Integration?hsLang=en).

#### 👥 For Retailers:

To learn more about how to integrate receiving shipments from your partners using the EDI format see this link.

**CSV**

[Download CSV Samples](https://support.logicbroker.com/hubfs/logicbroker_media/Logicbroker_Shipment_CSV_Samples.zip?hsLang=en)

Click the link above to download the CSV samples. Note by default if you are retrieving shipments from Logicbroker's SFTP/FTP a simplified version will be provided, the sample is annotated with **EXPORT**.

To receive the format as listed below in the Field Descriptions, please contact [support@logicbroker.com](mailto:support@logicbroker.com). All fields listed below reflect the model schema for the Logicbroker standard CSV format. For example the snippet below would match the field name **ShipToAddress.CompanyName** in the Field Descriptions below.
    
    
    Id,ShipToAddress.CompanyName
    221804,Merchant Co
    

If there is a field that is missing in the structure you can add custom fields as an extended attribute on the header level or item level; see example below. Note when a custom field is added, you will need to notify Logicbroker to ensure it is mapped to your partners.
    
    
    Id,ExtendedAttribute[Name=EXAMPLE].Value
    221804,Portal
    

The value in the field descriptions documentation will show as **ExtendedAttribute.EXAMPLE** and for line items **ShipmentLine.ExtendedAttribute.EXAMPLE**

#### ✨Tip:

When submitting or receiving a **CSV** shipment, each row will be split out for each line item and unique package. Therefore, if one line item is shipped in 2 packages there would be 2 rows for that line indicating a different TrackingNumber or ContainerCode for each row. If you are submitting a Shipment to Logicbroker for creation, the line items will get consolidated into one shipment and containers created appropriately if they share the same **ShipmentNumber.**

All shipments must include package/carton information. There is a header level **ShipmentInfos** which will be used to define pallet information and item level **ShipmentLine.ShipmentInfo** which indicate quantity shipped and other container info per each package/carton; this is always required. An example of the different hierarchies is shown below:

##### Standard (No Pallet)

Quantity will always be provided per package in **ShipmentLine.ShipmentInfo.Qty** and **ShipmentLine.ShipmentInfo.TrackingNumber** will indicate the package/carton the item is shipped in. 

In the example you can see one line item, is being shipped in 2 different boxes. This will create a shipment with one line containing 2 **ShipmentInfos** \- 2 container/cartons with a total quantity shipped of 20. Being that **ShipmentNumber** is the same across rows it will create one document. In addition, being that the **ShipmentLine.ItemIdentifier.SupplierSKU** is the same with different TrackingNumbers across multiple rows will create that one line with multiple cartons.
    
    
    ShipmentNumber,PartnerPO,ShipmentLine.LineNumber,ShipmentLine.ItemIdentifier.SupplierSKU,ShipmentLine.ShipmentInfo.TrackingNumber,ShipmentLine.ShipmentInfo.ContainerCode,ShipmentLine.ShipmentInfo.Qty  
    SH111111111111,PO1112222,1,V-123SKU,TRK1Z000001,081034001000008795,15  
    SH111111111111,PO1112222,1,V-123SKU,TRK1Z000002,081034001000008765,5

##### With Pallet

In this example you can see a pallet is identified by the ShipmentInfo.ContainerCode and the package/carton is associated to the pallet by sharing the same code in **ShipmentLine.ShipmentInfo.ShipmentContainerParentCode.**
    
    
    ShipmentNumber,PartnerPO,ShipmentLine.LineNumber,ShipmentLine.ItemIdentifier.SupplierSKU,**ShipmentInfo.ContainerCode,ShipmentLine.ShipmentInfo.ShipmentContainerParentCode,** ShipmentLine.ShipmentInfo.TrackingNumber,ShipmentLine.ShipmentInfo.ContainerCode,ShipmentLine.ShipmentInfo.Qty  
    SH111111111111,PO1112222,1,V-123SKU,00086275400000051600,00086275400000051600,TRK1Z000001,081034001000008795,15  
    SH111111111111,PO1112222,1,V-123SKU,00086275400000051600,00086275400000051600,TRK1Z000002,081034001000008765,5

#### 🚚 For Suppliers:

To learn more about how to integrate sending shipments using the CSV format see this [link](/kb/logicbroker/360022057591-Step-6-Testing-Your-Integration?hsLang=en).

#### 👥 For Retailers:

To learn more about how to integrate receiving shipments to your partners using the CSV format see this link.

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
BSN102 |  **ShipmentNumber** |  Unique ID to identify the shipment. |  **Required**  
BSN103 |  **ShipmentDate** |  Date units are shipped |  **Required**  
N/A |  **DocumentDate** |  Date the document was created. This field will automatically default with the date the document is created. |  **Required**  
HL*O:PRF01 |  **PartnerPO** |  This will be the purchase order number, this will be the main Key to link all your documents. This should match the order. |  **Required**  
HL*O:PRF04 |  **OrderDate** |  Date on the Purchase Order |  **Optional - will be pulled from original order if not provided**  
N/A |  **OrderNumber** |  Contains the end customer's order number, this will be used on the packing slip. |  **Optional**  
REF02 (BM) |  **BillofLading** |  Document number issued by the carrier which contains details of the shipment. |  **Conditional - if available**  
REF02 (CN) |  **PRONumber** |  Typically used by LTL freight carriers, A PRO number is a series of numbers used by carriers as a reference for freight movement; this is like a tracking number. |  **Conditional - if available**  
REF02 (IA) |  **VendorNumber** |  This is the internal vendor number provided to the supplier from the merchant. If available it is always recommended to send. |  **Optional**  
N/A |  **Note** |  Notes or shipping instructions provided by supplier; see the meaning of the notes on the individual partners notes. |  **Optional**  
DTM02 (067) |  **ExpectedDeliveryDate** |  Date the shipment is expected to be received at the shipping location. |  **Required**  
N/A |  **Payments.Method** |  Shipment method of payment. Typical codes received are listed below: CC: Collect PO: Prepaid Only |  **Optional**  
N102 (SF) |  **ShipFromAddress.CompanyName** |  ShipFromAddress is not required if you have a rule in place to default for all shipments. |  **Required**  
N201 (SF) |  **ShipFromAddress.FirstName** |  |  **Required**  
N202 (SF) |  **ShipFromAddress.LastName** |  |  **Optional**  
N301 (SF) |  **ShipFromAddress.Address1** |  |  **Required**  
N302 (SF) |  **ShipFromAddress.Address2** |  |  **Required**  
N401 (SF) |  **ShipFromAddress.City** |  |  **Required**  
N402 (SF) |  **ShipFromAddress.State** |  |  **Required**  
N404 (SF) |  **ShipFromAddress.Country** |  |  **Optional**  
N403 (SF) |  **ShipFromAddress.Zip** |  |  **Required**  
N104 (SF*92) |  **ShipFromAddress.AddressCode** |  |  **Optional**  
N1:PER06 (TE) |  **ShipFromAddress.Phone** |  |  **Optional**  
N1:PER04 (EM) |  **ShipFromAddress.Email** |  |  **Optional**  
HL*T:MAN02 (GM) |  **ShipmentInfo.ContainerCode** |  SSCC-18 and Application Identifier to be used to identify the pallet. If not provided the tracking number can be used. To identify what cartons belong to the pallet, you will need to enter this value in the "ParentContainerCode" under the "ShipmentInfos" (containers) on the line level. |  **Conditional - only required if sending a pallet**  
HL*T:TD101 |  **ShipmentInfo.ContainerType** |  Use "PLT" to Specify Pallet |  **Conditional - only required if sending a pallet**  
HL*T:REF02 (ZH) |  **ShipmentInfo.TrackingNumber** |  |  **Conditional - only required if sending a pallet**  
HL*T:TD107 |  **ShipmentInfo.Weight** |  Total gross weight of the package or carton. |  **Conditional - only required if sending a pallet**  
HL*T:TD108 |  **ShipmentInfo.WeightUnit** |  Weight Unit of Measure for the package or carton. |  **Conditional - only required if sending a pallet**  
HL*T:TD109 |  **ShipmentInfo.Length** |  Length of the container or package. |  **Conditional - only required if sending a pallet**  
HL*T:TD109 |  **ShipmentInfo.Width** |  Width of the container or package. |  **Conditional - only required if sending a pallet**  
HL*T:TD109 |  **ShipmentInfo.Height** |  Height of the container or package. Should be provided in inches. |  **Conditional - only required if sending a pallet**  
HL*T:TD110 |  **ShipmentInfo.DimensionUnit** |  Dimension unit of measure used for Length, Height and Width. |  **Conditional - only required if sending a pallet**  
N/A |  **ExtendedAttribute.EXAMPLE** |  |   
HL*I:PID05 (08) |  **ShipmentLine.Description** |  Standard short description or name of the product. |  **Optional**  
N/A |  **ShipmentLine.Quantity** |  Will be copied from the QTY Shipped provided under Shipment Infos. |  **Read Only**  
HL*I:LIN101 |  **ShipmentLine.LineNumber** |  Line Number from the Order. If not provided this will be taked from the order automatically. |  **Required**  
HL*I:SN103 |  **ShipmentLine.QuantityUOM** |  Unit of measure to identify the quantity in the container or package. |  **Required**  
N/A |  **ShipmentLine.Price** |  Unit cost that the merchant expects to be billed for each unit fulfilled. |  **Optional**  
HL*I:LIN105 (IN) |  **ShipmentLine.ItemIdentifier.PartnerSKU** |  The Item identifier that is internal to the purchaser/merchant. |  **Conditional - if received on an order this value should be returned**  
N/A |  **ShipmentLine.ItemIdentifier.ManufacturerSKU** |  Manufacturer's ID for the product. |  **Conditional - if received on an order this value should be returned**  
N/A |  **ShipmentLine.ItemIdentifier.ISBN** |  International Standard Book Number |  **Conditional - if received on an order this value should be returned**  
HL*I:LIN103 (VN) |  **ShipmentLine.ItemIdentifier.SupplierSKU** |  The Item Identifier that is used by the supplier or the person fulfilling the product. This will always contain a value. |  **Required**  
HL*I:LIN07(UP) |  **ShipmentLine.ItemIdentifier.UPC** |  Typically the U.P.C Consumer Package code will be provided; however additional standardized codes can be provided here as well. See specific partner instructions for details. |  **Conditional - if received on an order this value should be returned**  
DTM02 (011) |  **ShipmentLine.ShipmentInfo.DateShipped** |  Date the package was shipped. This will updated all header DateShipped values. |  **Required**  
HL*P:MAN02 (GM) |  **ShipmentLine.ShipmentInfo.ContainerCode** |  SSCC-18 and Application Identifier to be used to identify the child container. Field is required, hoewever if no value is provided the tracking number will be used as the container code.  |  **Conditional - Only required if partner requires GS1-128**  
HL*I:SN102 |  **ShipmentLine.ShipmentInfo.Qty** |  Total Qty of the product within the package or container. This quantity will be summed up across all containers and the total will be supplied on the item level "Quantity" field. |  **Required**  
HL*P:MAN02 (CP) |  **ShipmentLine.ShipmentInfo.TrackingNumber** |  Tracking number Identifier provided from the carrier to be used to identify the container. If no container code is being used, this will be used as the container code. |  **Required**  
TD503 |  **ShipmentLine.ShipmentInfo.CarrierCode** |  This will typically be the Standard Carrier Alpha Code (SCAC). If you are using your own custom shipping methods to map "CarrierCode" and "ServiceLevelCode" then this will not be required, however the proper mapped code will need to be provided in the ClassCode. |  **Required**  
TD505 |  **ShipmentLine.ShipmentInfo.ClassCode** |  The shipping method that will be used to send the merchandise. This can be a free form field or if using the shipment code mappings will need to match the Custom Code that was setup. When sending the Custom Code, the corresponding CarrierCode and Class Code will automatically get populated. |  **Required**  
TD512 |  **ShipmentLine.ShipmentInfo.ServiceLevelCode** |  Service Level set to ship by the carrier. Check with trading partner to see applicable codes. An example of a few would be: ND = Next Day CG = Ground ON = Overnight SA = Same Day If you are using your own custom shipping methods to map "ServiceLevelCode" then you will not need to provide the value, however the proper mapped code will need to be provided in the ClassCode. |  **Optional**  
N/A |  **ShipmentLine.ShipmentInfo.ShipmentContainerParentCode** |  SSCC-18 and Application Identifier to be used to identify the pallet. If you are shipping a pallet and need to identify which cartons belong to it, this value needs to match the container code provided on the pallet in the header level "ShipmentInfo" |  **Optional**  
HL*P:TD101 |  **ShipmentLine.ShipmentInfo.ContainerType** |  Specifies the code used to identify the package type. See specific trading partner for correct codes. "0" will indicate what number pallet is being used. Numbers will start at 0, and increment by 1. |  **Required**  
HL*P:TD107 |  **ShipmentLine.ShipmentInfo.Weight** |  Total weight of the package or carton. Default will be in pounds. |  **Required**  
HL*P:TD108 |  **ShipmentLine.ShipmentInfo.WeightUnit** |  Weight Unit of Measure for the package or carton. Default will be in pounds. |  **Optional**  
HL*P:PO410 |  **ShipmentLine.ShipmentInfo.Length** |  Length of the container or package. To be provided in inches. |  **Required**  
HL*P:PO411 |  **ShipmentLine.ShipmentInfo.Width** |  Width of the container or package. To be provided in inches. |  **Required**  
HL*P:PO412 |  **ShipmentLine.ShipmentInfo.Height** |  Height of the container or package. To be provided in inches. |  **Required**  
HL*P:PO413 |  **ShipmentLine.ShipmentInfo.DimensionUnit** |  Dimension for the values in Length, Width and Height fields. |  **Optional**