---
title: "Document Settings"
url: "https://support.logicbroker.com/kb/logicbroker/8058922786836-document-settings"
category: "Platform"
---

March 5, 2026

# Document Settings

## 

**Audience :** Suppliers

In this article, you will find information related to **Document Settings**. These are settings **suppliers** can set up to **automate** , **default** and **configure** document-specific settings to their account. The sections within this article are outlined below:

  * Payment Terms
  * Remittance Addresses
  * Ship From Addresses
  * Return Addresses
  * Acknowledgment Settings
  * Return Reasons
  * Shipment Settings



#### __ Note:

Some settings are only available to Logicbroker customers. These will be noted in the documentation provided below. To become a Logicbroker customer, click [here](https://www.logicbroker.com/company/contact-us/?__hstc=233546881.e1f5f40af0e38d651c4b286ccd3bffb6.1762765967593.1772694410339.1772704584277.86&__hssc=233546881.22.1772704584277&__hsfp=86f5b137dcb7b269b3ed43a0d78f3092).

### **Payment Terms**

**Payment terms** are the conditions surrounding the payment part of a sale, typically specified by the supplier to the retailer. The **Payment Terms** document setting allows suppliers to configure their payment terms on a general or partner-specific level and are applied to **invoices**. This saves users time when creating documents by not having to input these fields on each invoice.

**Payment Terms**

**Terms Description** – the description you choose for the payment terms you have established with your partner

**Net Days Due **– the number of days payment needs to be made from the invoice date

**Net Discount Days Due **– the number of days payment needs to be made from the invoice date in order for a discount to be applied

**Discount Percentage **– the discount percentage set forth by a supplier and retailer that is applied to invoices paid earlier than the due date

**Payment Terms are used in 3 scenarios**

  1.      1. **Portal invoices** \- suppliers that create**invoices** manually in the portal can have these settings defaulted on individual invoice documents after the invoice has been **submitted**
     2. **Auto-invoices** \- suppliers that have set up auto-invoicing can have these settings applied to invoices generated automatically off shipments _**Please note:**_ auto-invoicing is reserved for Logicbroker customers. See the **Shipment Settings** section of this article for more info
     3. **CSV/EDI/API** **invoices** \- suppliers using a non-portal integration method (CSV, XML, JSON, API, EDI) can have them applied to incoming invoices in the case that payment terms are not being sent through on documents



_**Please note:**_ If you send an invoice with any of the values below, then none will default. For example, if you send N30 in **PaymentTerm.TermsDescription** and have a value of "30" set for **Net Days Due** , the "30" will not default in **PaymentTerm.PayInNumberOfDays** . You will need to leave all values **blank** to have the fields default.

### **Remittance Addresses**

**Remittance Addresses** are the specific postal addresses that businesses use to receive payments and invoices by mail. The **Remittance Addresses** document setting allows suppliers to configure their remittance addresses on a general or partner-specific level and are applied to **invoices**. This saves users time when creating documents by not having to input these fields on each invoice.

### **  
Ship From Addresses**

**Ship From Addresses** are the specific postal addresses that orders are shipped out from. The **Ship From Addresses** document setting allows suppliers to configure their ship from addresses on a general or partner-specific level and are applied to **shipments**. This saves users time when creating documents by not having to input these fields on each shipment. Users can also use our **Address Book** tool to store multiple addresses to select from upon document creation - see the **Address Book** section of our [**Documents** ](/kb/logicbroker/7911726876308-Documents#h_01G8S4N23QTJH6ZBE97Y8V78PA)article for more information. 

### 

### **Return Addresses**

**Return Addresses** are the specific postal addresses that orders should be returned to in the case that a customer triggers the return process. The **Return Addresses** document setting allows suppliers to configure their return addresses on a general or partner-specific level and are applied to **return labels** in if they are mapped on **packing slips**.

### 

### **Acknowledgment Settings**

**Acknowledgment Settings** provide suppliers with some options on a general or partner-specific level and are applied to **acknowledgments**.

**Acknowledgment Settings**

**Default Days to Ship** – the number of days you expect to ship an order in

**Exclude Weekends **– toggling this on will exclude weekends from **Default Days to Ship** meaning that if you create an acknowledgment on Friday, your Default Days to ship will not consider the weekend when the information is sent to the retailer

**Default Cancellation Reason **– the reason that will be applied on all cancellation acknowledgments made in bulk or on individual orders _**Please note:**_ reach out to your partner to know which ones they accept

### 

### **Return Reasons**

The **Return Reasons** settings allows suppliers to configure their default return reason on a general or partner-specific level and are applied to **returns**. 

### 

### 

### **Shipment Settings**

**Shipment Settings** provide suppliers with some options on a general or partner-specific level and are applied to **shipments**.

**Shipment Settings**

**UCC128 (GS1) Company ID** – if you are working with a retailer that requires GS1 labels, this is where you will enter in your UCC128 Company ID used to generate the labels - these are normally required for bulk and replenishment orders. For more information on GS1 Labels and UCC 128 Company IDs, see [here](https://www.gs1-128.info/sscc-18/). 

***Copy Ship Method From Order **– toggle this on if you want **s****hip methods** on **shipments** to be defaulted to what the retailer sent on the order **_Please note:_ **you are still required to ship orders using the retailer-requested ship method **  
**

  *     * **Use Case** – Retailers may not accept certain ship methods or variations of the code that is sent. Suppliers can ship with the correct ship method and not have to worry about the code not matching up to exactly what the retailer is looking for.



***Create Invoice From Shipment **– toggle this on if you want complete shipments to trigger an invoice document to be created and sent out to the retailer on your behalf **_Please note:_ **invoices will be populated using a random invoice number **  
**

  *     * **Use Case** – Some retailers require invoice documents for all shipped orders. This feature allows for automation in creating and sending this document. Some retailers do not accept invoices and require suppliers to invoice outside of Logicbroker. This configuration does not support those instances. Auto-invoicing generates a random invoice number. If the supplier needs a specific invoice number to be sent, this configuration will not work.



**_Please note:_ **Settings with an asterisk are reserved for Logicbroker customers. To become a Logicbroker customer, click [here](https://www.logicbroker.com/demo-request/).