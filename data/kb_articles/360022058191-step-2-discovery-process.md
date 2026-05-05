---
title: "Step 2: Discovery Process"
url: "https://support.logicbroker.com/kb/logicbroker/360022058191-step-2-discovery-process"
category: "Retailer Onboarding"
---

March 10, 2026

# Step 2: Discovery Process

## 

When integrating with Logicbroker, we walkthrough a detailed discovery process to understand your integration capabilities and what Logicbroker platform features will work best for your process.

Beginning with the survey results provided in the previous step, our **onboarding team** will go through the information provided and schedule a meeting with all **stakeholders** to gather additional information and answer any questions regarding your business flow. From there we can build a **solution plan** posting to our project management software for full project visibility. Included with all potential solutions, our team will demo options so your team can get any answers to questions and view integration possibilities.

Below is a quick overview of our process for getting required data about your business.

  * Business Flow and Documents Supported
  * Integration Options
  * Partner Communication
  * Reporting and Vendor Compliance



##### Business Flow and Documents Supported

Going through all the documents you plan to support with your integrated **suppliers/channels** we will look through any **sample documents** or **specifications** provided and begin showcasing available options for your process. This will include a view into how everything will look from the retailer's perspective and the process for suppliers/channels.

#### ✨Tip:

Before beginning the discovery process, make sure all **sample documents** and **specifications** are provided to the Logicbroker onboarding team. This will help provide direction when implementing your solution.

### Orders

Starting with orders we first determine if there is any **routing logic** required with your flow. Routing is used to determine which supplier(s) will receive purchase orders when an item is ordered for drop ship. Logicbroker has the ability to consume **sales orders** received from any platform (eCommerce, OMS, ERP, etc) and use the data for simple or complex routing logic to send each item on the sales order to the **best matched supplier**. These rules can be by lowest cost, SKU, availability, location, etc.

We also determine what type of orders will be sent to your suppliers/channels. Logicbroker has the ability to support standard **dropship** , store **replenishment** , **warehouse replenishment** , **warehouse transfers** , etc. Each order type may have different requirements and all can be handled to provide the correct data to your suppliers.

In addition, to flow of document information we will determine what data will always be **required** and **transmitted** to your suppliers/channels. This will help us build **specifications** and **validation** to ensure your suppliers always receive the correct data. When an order is integrated into our system all standard integration options are available to you supplies; this includes Portal, CSV, XML, EDI, JSON, etc.

### Acknowledgements

In Logicbroker Acknowledgements are used by your supplier/channels to **accept** , **cancel** , or **backorder** items. This document is optional and the features can be limited based on your needs. For example, you can use the document to be only used for cancellations and/or backorders. This will depend on the capabilities of your system. In addition, rules can be put in place to add validation for only "**kill or fill** " processing or limiting **partial** order cancellations. Support for both retailer or supplier initiated cancellations can also be added.

When an Acknowledgement is integrated into our system all standard integration options are available to you supplies; this includes Portal, CSV, XML, EDI, JSON, etc.

### Shipments

In Logicbroker, shipments are used to update your orders with all **tracking** and **packaging** information for all ordered items shipped. Based on the type of orders you will be sending different shipment data may be required. It is important for us to determine what those different data requirements might be, this can be differences between **freight shipments** and **parcel carriers** , **service levels** and **carriers** are supported, or **validation** to allow/reject partial shipments.

When a shipment is integrated into our system all standard integration options are available to you supplies; this includes Portal, CSV, XML, EDI, JSON, etc.

### Invoices

In Logicbroker, the invoice is used to bill the retailer for orders fulfilled. Invoices may not always be required, but if enabled may include different requirements based on your flow. This can include **partial invoicing** , allow invoicing before shipments, including **shipment data** on the invoice, and/or including additional **discounts** and **charges** (handling, tax, etc).

When an invoice is integrated into our system all standard integration options are available to you supplies; this includes Portal, CSV, XML, EDI, JSON, etc.

### Returns

In Logicbroker, returns are used to communicate that a supplier has received a return for a retailer's order. When walking through your return process, our team will need to understand if **physical returns** will be received in warehouse, at **supplier's location** and what data will need to be transmitted when received.

Again your return process can differ between order type and **Service Level Agreements** (SLA) with your suppliers. Based on this, rules can be put in place to allow only certain types of returns, require specific data (**return shipment information** , **return reason codes** , etc), or prevent returns with no fulfillment data.

When a return is integrated into our system all standard integration options are available to you supplies; this includes Portal, CSV, XML, EDI, JSON, etc.

### Inventory

Inventory is used to update your system with all available product quantities. Logicbroker will need to know **how often** you will receive this data, what specific information is required (**quantity** , **status** , **price/cost** , **item identifiers** , etc), how products will be **setup** , and what type of updates (**delta** , **full product feeds** , **split per supplier** , etc). This will depend on yours system's capabilities as Logicbroker can support validating all updates against the products setup in our system or allow free flowing of inventory data from all suppliers with limited validation.

When inventory is integrated into our system all standard integration options are available to you supplies; this includes Portal, CSV, XLSX, and API.

### Product Content

Product Content is used to collect and transmit all product data from your suppliers/channels. This can include **images** , **descriptions** , **dimensions** , **ingredients** , etc. Content can be customized on product category and enable format requirements for all your suppliers to follow. Please see [this article](/kb/logicbroker/360023030132-Product-Content-Product-Feeds?hsLang=en) for more information on using product content.

### Other Documents and Information

In some cases, other required data may be important to provide or receive from/to your suppliers. Here is a quick list of other information that can be transmitted.

  * **Packing Slips:** Custom packing slips can be created and provided to your suppliers on all orders sent. These can be used for picking and inserted in all shipment packages.
  * **GS1 Labels:** GS1 labels are used on all boxes that are shipped. The bar code matches the data sent on the Shipment document. This will allow your system to match orders sent to your warehouses or stores for pickup or replenishment.
  * **Carrier Postage Labels:** These are standard labels that can be created by your suppliers using your carrier account. This will allow you to control supply chain costs and give your supplier an easy way to print carrier labels in our system when fulfilling orders.



#####   
Integration Options

Logicbroker offers any integration option to automatically send and receive all your document types. Below are some examples of options. These can be mixed and matched with all **document types** and inserted into your **workflow**. Gathering samples will be important for our onboarding team to setup standard specifications for all your suppliers.

  * **Logicbroker REST API** : Follow [documentation here](https://dev.logicbroker.com/#55441eed-350c-dedf-cccd-d842ebf81e28) for setting up an integration as a retailer.
  * **Logicbroker Standard XML, JSON, CSV, EDI** : You can follow our standard specifications [shown here](/kb/logicbroker/document-standards?hsLang=en) for schema and format. For more information on connectivity options see [this section](/kb/logicbroker/document-standards#connection-information).
  * **Custom XML, JSON, CSV, EDI** : Logicbroker can use any supplied format which can be mapped to our internal system. These can be supplied using SFTP/FTP, HTTPS, AS2 (EDI Only), or VAN (EDI Only). For more information on connectivity options see [this section](/kb/logicbroker/document-standards#connection-information).
  * **Custom API** \- We can also customize REST API endpoints for your needs as well. This includes GET, POST, DELETE methods with custom requests and responses that can simulate any existing APIs you already use.



##### Partner Communication (Knowledgebase + Onboarding)

Understanding how communication will be transmitted to all your suppliers will be important to make sure your suppliers are supported on all levels of their integration process. This includes **onboarding communication** , **providing integration details** , **supplier updates** and **standard support**. Listed below are some features to assist in what information we will gather during the discovery process.

**Onboarding Communication:** Need to define who will manage the communication to all suppliers being onboarded. Logicbroker can initiate all contact between your suppliers, providing a full onboarding package which includes a welcome email, survey and direct contact to our onboarding specialists. Or this can be managed by your team which details can be provided for your team to manage.

**Support and Knowledgebase:** A custom KB can be hosted by Logicbroker with all your custom branding/styling giving all your suppliers access to integration information and setup processes. The knowledgebase can be used to customize articles, providing any type of information to your suppliers and channels to help integrating their system with yours.  
A pathway will also be provided for support as well, including a specific support email to open tickets. Our support team can answer any integration questions and relay business questions to the appropriate retailer contact.

**Supplier Updates:** Messaging to all suppliers can also be enabled on the platform. Messages can be broadcasted to all suppliers through our portal allowing for full communication. This can be managed by your retailer team or Logicbroker can initiate messages on your behalf.

**Customized Walkthroughs:** Custom walkthroughs can be created for your suppliers or support team. This can help them get acclimated with the Logicbroker platform. Tooltips will guide users and help monitor and accomplish tasks.

##### Reporting and Vendor Compliance

Out of the box Logicbroker offers reports that can be customized in our system or advanced reports can be created to provide a full view of **vendor compliance**. Understanding what data you need to **monitor** will help us **collect** and **build** reporting for you and all your suppliers. Listed below is a quick overview of reporting that is available to assist in what information may be required during the discovery process.

**Basic Reporting:** Used for creating charts based on order counts and GMV or monitoring and filtering documents. For more information on using basic reporting see this article.

**Score Cards:** Provides a general view of all your suppliers and how well they are performing based on shipment time, percent shipped and percent cancelled. Each metric is weighted to provide a letter score (A+ to F) for each supplier. Your suppliers will have visibility to this as well. For more information see [this article](/kb/logicbroker/360021857932-Scorecard?hsLang=en).

**Advanced Export:** You can export document data out of the Logicbroker portal, customizing your own CSV exports. This can be useful for creating reports outside of the Logicbroker system. For more information see [this article](/kb/logicbroker/360021857892-Advanced-Export?hsLang=en).

**Advanced Reporting:** Logicbroker can provide a dedicated reporting dataset used with Microsoft's Power BI. Custom reports can be created using data from other systems and creating custom metrics to provide detailed analysis of how your suppliers are performing. This can include, % of orders shipped, how often inventory is updated, Shipping analysis on delivery times, etc. These reports can be viewed in the portal. For more information see [this article](/kb/logicbroker/360022068551-Analytics?hsLang=en).