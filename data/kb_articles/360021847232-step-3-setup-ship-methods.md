---
title: "Step 3: Setup Ship Methods"
url: "https://support.logicbroker.com/kb/logicbroker/360021847232-step-3-setup-ship-methods"
category: "Supplier Onboarding"
---

March 10, 2026

# Step 3: Setup Ship Methods

## 

Logicbroker offers the ability to map your custom shipment method codes on Orders and Shipments to the standard codes within the platform. When receiving an order from your channel/retailer, you can use the standard codes to map to your existing (custom) codes available in your system. 

Shipping methods are normally defined by their **carrier** and **service level**. To simplify the identification of both, we consolidate the two (carrier and service level codes) into one **standard code**. This **standard code** can then be mapped to a custom identifier set by you to receive on Orders and send on Shipments. Creating this mapping will ensure the correct codes (both carrier and service level) will be sent to your channel/retailer in full compliance. 

#### ✨Tip:

You can avoid mapping shipment codes and have all codes for shipments defaulted to what is received on the order. Contact [support](mailto:support@logicbroker.com) to have this configured for all of your channels/retailers.

All available standard codes are shown under **Settings** > [Shipment Options](https://stageportal.logicbroker.com/shipment-options)

If you plan on using a custom code, you will need to set these up in both [stage](https://stageportal.logicbroker.com/shipment-options) and [production](https://portal.logicbroker.com/shipment-options) environments.

You can see which standard codes are available by your channels/retailers by the **Used by Partner** check box. The codes checked are ones you should expect to receive on orders and required codes to send on shipments. 

Click **Edit** to add your custom codes for automatic mapping on the order and shipment documents. Once these are set you will receive the code on orders and can send them on shipments. For more details on how which field to add these continue below to How Shipment Method Mappings work.

##### How do Shipment Method Mappings work?

Receiving or sending your codes will differ depending on the standard format you are integrating with. Below shows how ship methods are provided for each integration format. For more details visit the document specifications for [Orders](http://help.logicbroker.com/hc/en-us/articles/360021847952-Order-Specifications?hsLang=en) and [Shipments](http://help.logicbroker.com/hc/en-us/articles/360022058371-Shipment-Specifications?hsLang=en).

**Portal**

In the portal, if the mapping is setup and receive an order with the **standard** code, you will see your **custom** code under the **Shipping & Payment Information** section. If there is no code setup, you will see the Logicbroker **Standard** code. If the channel/retailer does not use standard codes, the raw value will be shown. 

When creating **shipments** , you can either enter a **Standard c** ode or your **custom** code under the **Packages** section. The **Standard** code can be selected from the drop down for normal parcel carriers, or a **custom** code can be entered in free form. 

**JSON**

For receiving **orders** from your channels/retailers you will see your shipment method information in the header **ShipmentInfos** array. This will be shown in the first **ShipmentInfo** object.   
  
**ReceiverClassCode** will be your custom code if one is setup.   
  
**ClassCode** will be the Logicbroker Standard Code or the raw channel/retailer code if one is not mapped to the standard.   
  
**SenderClassCode** will be the raw code originally sent by the channel/retailer. 
    
    
    {
      "ShipmentInfos": [
        {
          "ReceiverClassCode": "CUSTOMCODE",
          "ClassCode": "UPSN-CG",
          "SenderClassCode": "UPS Ground"
        }
      ]
    }

When sending **Shipments** , all **ShipmentInfos** under the **ShipmentLine** should contain the **ClassCode** value. This can be either a Logicbroker **Standard Code** or **Custom Code** that was setup in the **Shipment Method Mappings**. 
    
    
    {
      "ShipmentLines": [
        {
          "ItemIdentifier": {
            "SupplierSKU": "V-123123"
          },
          "ShipmentInfos": [
            {
              "DateShipped": "2019-01-01T12:00:00",
              **"ClassCode" : "CUSTOMCODE",**
              "TrackingNumber": "TRK11111",
              "ContainerCode": "00086275400000051594",
              "Qty": 15,
              "ContainerType": "CTN",
              "Height": 1.0,
              "Width": 2.0,
              "Length": 3.0,
              "DimensionUnit": "IN",
              "Weight": 0.0,
              "WeightUnit": "LB"
            }
          ],
          "Quantity": 15,
          "QuantityUOM": "EA",
          "LineNumber": "1"
        }
      ]
    }
    

**XML**

For receiving **orders** from your channels/retailers you will see your shipment method information in the header **ShipmentInfos** array. This will be shown in the first **ShipmentInfo** object.   
  
**ReceiverClassCode** will be your custom code if one is setup.   
  
**ClassCode** will be the Logicbroker Standard Code or the raw channel/retailer code if one is not mapped to the standard.   
  
**SenderClassCode** will be the raw code originally sent by the channel/retailer. 
    
    
    <Shipment xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <ShipmentInfos>
        <ShipmentInfo>
            <ClassCode>FDEG_GD</ClassCode>
            <ReceiverClassCode>CUSTOMCODE</ReceiverClassCode>
            <SenderClassCode>FedEx Ground</SenderClassCode>
        </ShipmentInfo>
    </ShipmentInfos>
    </Shipment>

When sending **Shipments** , all **ShipmentInfos** under the **ShipmentLine** should contain the **ClassCode** value. This can be either a Logicbroker **Standard Code** or **Custom Code** that was setup in the **Shipment Method Mappings**. 
    
    
    <Shipment xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
      <ShipmentLines>
        <ShipmentLine>
          <ItemIdentifier>
            <SupplierSKU>V-123123</SupplierSKU>
          </ItemIdentifier>
          <ShipmentInfos>
            <ShipmentInfo>
              <DateShipped>2019-01-01T12:00:00</DateShipped>
    ** <ClassCode>CUSTOMCODE</ClassCode>**
              <TrackingNumber>TRK11111</TrackingNumber>
              <ContainerCode>00086275400000051594</ContainerCode>
              <Qty>15</Qty>
              <ContainerType>CTN</ContainerType>
              <Height>1</Height>
              <Width>2</Width>
              <Length>3</Length>
              <DimensionUnit>IN</DimensionUnit>
              <Weight>0</Weight>
              <WeightUnit>LB</WeightUnit>
            </ShipmentInfo>
          </ShipmentInfos>
          <Quantity>15</Quantity>
          <QuantityUOM>EA</QuantityUOM>
          <LineNumber>1</LineNumber>
        </ShipmentLine>
      </ShipmentLines>
    </Shipment>
    

**EDI**

For receiving **orders** from your channels/retailers you will see your shipment method information in the header **TD505** element. The TD505 will auto-populate with the Custom Code if one is setup, if not the Standard Code will be used, and if neither is a available the raw original value will be sent. **TD503** will auto populate with the standard carrier code and **TD512** will auto-populate with the standard service level code as well.   

    
    
    TD5**2*UPSN** **CUSTOMCODE** *******CG~

When sending **Shipments** , the **TD505** element under the Shipment HL loop will need to be provided. This can be either a Logicbroker **Standard Code** or **Custom Code** that was setup in the **Shipment Method Mappings**. 
    
    
    HL*1**S~  
    TD5*B*2*UNSP** **CUSTOMCODE** *******CG~
    

**CSV**

For receiving **orders** from your channels/retailers you will see your shipment method information in the **ShipMethod** column. The **ShipMethod** will auto-populate with the Custom Code if one is setup, if not the Standard Code will be used, and if neither is a available the raw original value will be sent.  

    
    
    Id,ShipMethod  
    221804,**CUSTOMCODE**

When sending **Shipments** , the **ShipmentLine.ShipmentInfo.ClassCode** column will be used to populate the your ship method. This can be either a Logicbroker **Standard Code** or **Custom Code** that was setup in the **Shipment Method Mappings**. 
    
    
    ShipmentNumber,**ShipmentLine.ShipmentInfo.ClassCode**  
     SH_221804,**CUSTOMCODE**