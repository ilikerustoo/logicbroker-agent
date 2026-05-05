---
title: "Shipment Options"
url: "https://support.logicbroker.com/kb/logicbroker/360022068771-shipment-options"
category: "Platform"
---

March 10, 2026

# Shipment Options

## 

**Audience :** All users in Logicbroker. 

In this article, you will find information related to **Shipment Options**. Suppliers can create box presets and suppliers and retailers can view partner ship methods and map their own custom codes. The sections within this article are outlined below:

  * Boxes
  * Ship Methods



### **Boxes**

The **Boxes** section allows suppliers to configure their commonly-used box dimensions as presets. This saves users time when creating documents by not having to input these fields on each shipment. For more information on shipments including fields, settings and instructions on individual document creation, see our **[Shipments](/kb/logicbroker/7973910593940-Shipments?hsLang=en) **article.

  * **New Box** : to add a new box, click on New Box > enter in what you want to name it and the dimensions - you'll still have to input weight on shipments since this may vary depending on what is in the box 
  * **Edit/Delete Address** : click on **Edit** or **Delete** to make changes to your saved boxes or remove them



  * **See it in action** : Once you set up a box preset, you will see a dropdown in the **Box/Packages** section of shipments. Click on the dropdown > select you preset > see dimensions reflected > enter in your box weight



### **Ship Methods**

**Ship Methods** are the way in which information is communicated through partners about how an order will be shipped. Every partner has their own way of expressing a specific carrier and service level through a variety of codes and descriptions. Logicbroker’s ship method mappings function allows suppliers and retailers to map their unique **custom codes** to our **standard codes**.

Creating this mapping will ensure the correct codes (both carrier and service level) will be sent to your partner in full compliance.

#### __ ✨Tip:

Suppliers can avoid mapping custom codes and have all codes for shipments defaulted to what is received on the order. This is a Logicbroker Direct feature, to learn more about this offering, see [Logicbroker Direct](/kb/logicbroker/4408344934676-How-it-Works?hsLang=en) (scroll down to Features and Their Use Cases > Portal Configurations > Copy Ship Method from Order to Shipment)

**Definitions**

**SCAC** – stands fo **Standard Carrier Alpha Code**

**Ship Method** – the method of delivering a product to a customer-defined by **carrier** and **service level** \- this may often show as the **standard code** in the portal

**Service Level** – expresses the duration of transportation

**Carrier **– the party that transports the goods. While the carrier may be FedEx, the **Carrier Code** may be FDEG

**Standard Code** – the service level and carrier consolidated into one code. _**For example,**_ FDEG-CG (where the carrier is FedEx, FDEG and the service level is Ground, CG).

**Custom Code** – the code a partner uses to define a specific carrier and service level - this is how the ship method is set up in a partner’s external system

**Receiver Class Code** – the code the receiver of the document lists as the ship method - for orders, the receiver is the supplier and for shipments, the receiver is the retailer

**Sender Class Code** – the code the sender of the document lists as the ship method -for orders, the sender is the retailer and for shipments, the sender is the supplier

**Description** – the written-out ship method with no codes. _**For example,**_ FedEx Ground

**Example**

Take the ship method **FedEx Ground**. The carrier is **FedEx** and the service level is **Ground**. 

Each partner defines **FedEx Ground** with their unique **custom code** :

  *     * **Retailer** : FDEG-GR
    * **Supplier** : fedex_ground



**Logicbroker** defines this ship method with the **Standard Code** : FDEG-CG (for a full list of our Standard Codes, in the portal navigate to **Settings** > **Shipment** **Options** > review the first column).

*If a supplier or retailer uses a code that is different to our Standard Code to refer to the same ship method, their codes are known as **Custom Codes**. 

Depending on the document that is being traded (order or shipment), the code is also known as the **sender class code** or the **receiver class code**. 

In order for a retailer to send their custom code and the receiver to understand what that code means in their system and send back the respective code, both the retailer and the supplier need to have their unique custom codes mapped within Logicbroker.

**Order Flow**

The following diagram shows the **order** flow in relation to ship method mappings from the**R** **etailer’s** point of view.  
  


  1.      1. Retailers will send in **Orders** with a ship method using their **Custom Code**
     2. Logicbroker translates the **Custom Code** to a **Standard Code**
     3. Logicbroker sets the **Standard Code** on the **Order**
     4. Before the **Order** leaves the system, Logicbroker translates the **Logicbroker****Standard Code** to the supplier’s **Custom Code**



**Shipment Flow**

The following diagram shows the **shipment** flow in relation to ship method mappings from the **Supplier’s** point of view.   
  


  1.      1. Suppliers will send in **Shipments** with a ship method using the **Custom Code** they configured
     2. Logicbroker translates the **Custom Code** to a **Standard Code**
     3. Logicbroker sets the **Standard Code** on the **Shipment**
     4. Before the **Shipment** leaves the system, Logicbroker translates the **Logicbroker Standard Code** to the retailer’s **Custom Code**