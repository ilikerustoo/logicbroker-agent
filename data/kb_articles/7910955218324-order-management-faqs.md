---
title: "Order Management FAQs"
url: "https://support.logicbroker.com/kb/logicbroker/7910955218324-order-management-faqs"
category: "Platform"
---

March 13, 2026

# Order Management FAQs

## 

Below you will find the most frequently asked questions for order management, please click on the headings below to be directed to the specific section. 

  * Dashboard and Omnisearch
  * Orders Page
  * Documents
  * Bulk Actions
  * Orders
  * Acknowledgments
  * Shipments
  * Invoices
  * Returns



### **Dashboard and Omnisearch**

**Do I need to monitor the dashboard if I am not a portal user?**

_Yes. Even if you don't go into Logicbroker's portal to process orders, you should still monitor the dashboard page for**Noncompliant** documents. This will let you know if there are any errors with any orders or related documents - failed documents will not be transmitted to your system or your partner's system so it is important to monitor and troubleshoot._

**Can I customize my dashboard?**

_No. All users will have the same dashboard view although the data will change from a retailer/supplier perspective. If you are looking for more granular information and the ability to create, customize and export reports, use our**Standard Reporting** and [**Advanced Export**](/kb/logicbroker//360021857892-Advanced-Export?hsLang=en) tools. Some companies will also have access to **Advanced Analytics**. _

**Can I search documents using multiple criteria?**

_Yes. Logicbroker has a robust search functionality that allows you to**stack** search terms and use a **wildcard**. _

### **Orders Page**

**Can I multi-select documents from multiple pages on the Orders page?**

_No. Logicbroker’s filters on the**Orders** page go through our back-end Azure search function and is only per page meaning that the **Select all** function will only apply to the page you are on. If you want to perform actions on more documents than appear on the page, you can increase the **rows per page** in the bottom right of the screen. If you want to **export** more documents than appear on the page, you can use our **Advanced Export** tool._

**Will my display setting stick?**

_No.**Display** settings will only apply to your current session and will be removed once you refresh the screen. If you wish to have the same display settings, you'll need to re-configure them. _

**Do all actions apply to all documents?**

_No. Specific actions apply to certain documents. You will only see the**actions** button on **order** documents found in the right side of the screen on individual orders. When selecting documents (orders, shipments, invoices, etc.), you will see the applicable actions appear in the top bar of the screen._

### **Documents**

**Where can I see if a document was changed?**

_**Events** tab. On each document, you will see an **Events** tab - here is where you can see if a document as changed, failed, what action was taken, what user (if the chance happened in the portal) and a date and time stamp._

**I processed a shipment but didn't download the packing slip. Where can I find it?**

_**Attachments** tab. If you or your partner has an integration with a shipping label provider such as ShipEngine and are printing labels from the portal, you can head over to the **attachments** tab in the portal and download it from there in case you missed the pop-up window._

**Where can I see all documents associated with an order?**

_**Related Documents** tab. Head over to the **Related Documents** tab to see all related documents associated to the document you are viewing. You'll also see the internal Logicbroker **ID#** , the **date** and **time** it was created or received in/by Logicbroker, the **type** , **status** and **system**. _

### **Bulk Actions**

**Is there a limit to how many documents I can perform bulk actions on?**

_100\. If you are using the bulk actions found in the**Orders Page** , you can only perform **bulk** actions on the documents you select. If you change the **rows per page** , you'll see the max number of documents you can show on a page is 100. If you are looking to take action on more documents, use our [**Advanced Import**](/kb/logicbroker//360022068651-Advanced-Import?hsLang=en) tool._

**Do bulk actions have limitations?**

_Yes. Bulk actions do not support some options that may be available on individual order creation/processing such as scheduled ship dates, multiple boxes/tracking numbers etc._

**What documents can I download packing slips and GS1 labels?**

_Packing slips can be downloaded off orders and shipments. GS1 labels can only be downloaded from shipments._

### **Orders**

**Can Logicbroker route purchase orders to suppliers using line items on sales orders?**

_Yes. Logicbroker will create purchase orders and send them to suppliers based on the SKUs on the sales order._

**What should I do if my customer changed their ship-to address?**

_You cannot change address information on orders. In this case, the retailer would need to cancel the order and place a new one with the correct address._

### **Acknowledgments**

**What information can be shared on an acknowledgment?**

_Acknowledgments can be used to share accepted/cancelled/backordered information, change reasons and estimated ship/pickup dates. They cannot be used to change quantities or change order items._

**Does Logicbroker support 860s?**

_860s are used to change order information. Logicbroker does accept 860s and will show the document in the portal as a linked acknowledgment under the**order**. _

__

### **Shipments**

**What information is required on shipments?**

_Shipment fields are retailer-specific. While some retailers may require you to send information such as ship-from address, estimated delivery date, etc., other retailers may not require this. Review retailer-specific information and the[**Document Standards**](/kb/logicbroker//360054359431-Document-Standards-Validation-Rules?hsLang=en) tab in the portal to know what fields they require. _

### **Invoices**

**Where do I find my remittance address and remittance code?**

_For suppliers, the remittance address is the specific postal address that you'll use to receive payments and invoices by mail. Reach out internally for your remittance code - in some cases you'll need to reach out to your partner to see if they have configured one in their system._

### **Returns**

**Where can I find returns?**

_Returns can be found in the portal by searching 'Returns' in the search bar. You can also export return information using our[**Advanced Import**](/kb/logicbroker//360022068651-Advanced-Import?hsLang=en) tool._

**How can I tell which suppliers and products are most frequently returned?**

_Using our[**Advanced Import**](/kb/logicbroker//360022068651-Advanced-Import?hsLang=en) tool, you can export a report showing return document information including the supplier and returned items. Navigate to **Advanced Export** > select the **Profile** : Default Return Export > set your document **Filters** > configure your **Fields to Export** depending on the information you want to pull > **Download**. Once downloaded, you can use the information to find frequently-returned information by supplier and SKU. _

_Retailers that have access to**Advanced Analytics** can also use this tool to pull return information. Navigate to **Advanced Analytics** > **Supplier Details** tab > review return information in the far right. You will be able to see**Quantity Returned** and **Return %.**_

**How can I tell if the return was approved/rejected?**

_Suppliers would need to communicate**rejections** using our [**Message Center**](/kb/logicbroker//360022068611-Messages?hsLang=en) or reach out to the retailer outside of Logicbroker. If returns are accepted, suppliers can **Mark Items as Received** in the portal or create a **Return Response**. _

**How can I tell if the return was received?**

_Suppliers can**Mark Items as Received** in the portal notifying the retailer that the items have been successfully returned. _