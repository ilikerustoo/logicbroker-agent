---
title: "Acknowledgments"
url: "https://support.logicbroker.com/kb/logicbroker/7939700232980-acknowledgments"
category: "Platform"
---

March 12, 2026

# Acknowledgments

## 

**Audience :** All users in Logicbroker. 

In this article, you will find information related to **Acknowledgments**. The sections within this article are outlined below:

  * Overview
  * Acknowledgment Document
  * Acknowledgment Settings
  * Create an Acknowledgment (Acceptance, Backorder, Cancellation)



### **Overview**

Logicbroker identifies an Acknowledgment (EDI 855) as a document used to **accept** , **cancel** or **backorder** order items. This document is sent after the order is received and before the shipment or invoice is created/sent.

Retailers and suppliers send/receive acknowledgment information depending on how they are integrated with Logicbroker (EDI, API, JSON, XML, CSV, Flat File, Logicbroker Portal).​

**Acknowledgment Flow**

  1.      1. Once the supplier receives an order, they create/send an acknowledgment either accepting, cancelling or backordering order items
     2. Logicbroker transforms the data to a format the retailer accepts​
     3. Logicbroker sends the acknowledgment to the retailer



### **Acknowledgment Document**

From the portal, users can see documents regardless of the way they are integrated with our system. To see document details, search for the document using the **search bar** , click on it from the **Dashboard** or click **View** on the **Orders** page. See the acknowledgment document-specific details below. For general document information, see our **[Documents](/kb/logicbroker/7911726876308-Documents?hsLang=en) **article.

**Acknowledgment Fields**

**1 – Billing Address** – the address the end-customer used for billing 

**2 – Shipping Address** – the address the order should be shipped to – this can be a residential home, a business, an address code, etc. If sent on the order, the email and phone number will also appear here

**3 – General Information** – details carried over from the order and acknowledgement-specific information including: 

  *     * **Order ID** – the value the retailer assigns to the order
    * **Reference Number** – also known as the **Purchase Order Number** – typically the connecting identifier between all documents
    * **Acknowledgment Number** – unique identifier for each individual acknowledgement file that will be submitted. Logicbroker auto-populates this field but it can be modified as needed. **_Please note:_ **every acknowledgment should have a **unique** **Acknowledgement Number**. If you create more than one acknowledgment for an order, be sure to change this field in each document
    * **Change Reason** – **Cancellation Reason -** the reason why you are cancelling items. Select from the dropdown but make sure the reason you select is accepted by the retailer. If you are unsure which reasons are accepted by the retailer, reach out to the retailer directly **_Please note:_ **Logicbroker maps to retailer’s accepted cancel codes so your retailer’s specific code may not match what is in the dropdown. For example, a retailer may accept a code of **OS** to mean out of stock – in this case, Logicbroker will map our code to the retailer’s code so that when the supplier select the code **Out of Stock** from the dropdown, we will send it to the retailer as their accepted **OS**
    * **Requested Ship Date** – the date sent on the order that the retailer expects the order be shipped out by
    * **Estimated Ship Date** – the date you plan on shipping out the order by and should always be provided for acceptances and backorders - if there is more than one date due to multiple items being shipped out on different days or being on backorder, select the furthest day out
    * **Expected Delivery Date** – the date sent on the order that the retailer expects the order to arrive to the end consumer by
    * **Pickup Date** – the date the order is being picked up instead of shipped out. Normally this is for larger LTL or freight orders. Select the date from the calendar tool or type in the date using the provided format



**4 – Acknowledgment Items** – the order items being defined in the acknowledgement with Line, SKU, Partner SKU, UPC, Description, Quantity Accepted, Quantity Cancelled, Quantity Backordered and Change Reason 

### **Acknowledgment Settings**

There are a few **acknowledgment settings** you can configure in the portal. See below for details on requirements, configurations and how they work:

  * [Default Days to Ship](/kb/logicbroker/8058922786836-Document-Settings?hsLang=en)
  * [Default Cancellation Reason](/kb/logicbroker/8058922786836-Document-Settings?hsLang=en)



### **Create an Acknowledgement (Acceptance, Backorder, Cancellation)**

For detailed step-by-step instructions, see our **Create an Acknowledgment Quick Start Guide** below. 

[Create an Acknowledgment](https://support.logicbroker.com/hubfs/logicbroker_media/Create%20an%20Acknowledgment.pdf?hsLang=en)