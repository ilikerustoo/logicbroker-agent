---
title: "Introduction: What is Logicbroker?"
url: "https://support.logicbroker.com/kb/logicbroker/360022057491-introduction-what-is-logicbroker"
category: "Supplier Onboarding"
---

March 9, 2026

# Introduction: What is Logicbroker?

## 

Logicbroker is an integration platform that simplifies the processing of all supply chain data from retailers and suppliers. 

As a supplier, you will be using Logicbroker to receive orders from all of your retailers and channels. Our goal is to help you integrate all your order processing channels, whether its a big box retailer using EDI, marketplace or eCommerce platform, we have a full library of options to get you connected quickly. All documents and information will always be formatted in one canonical format allowing you to process data from 100s of different channels using one connection.

##### Document Types

[**Order**](/kb/logicbroker/360021847952-Order-Specifications?hsLang=en)

Will contain all information required to fulfill your orders; this includes addresses, Item identifiers, and quantities. Each order starts a new flow and all related documents submitted thereafter will be linked updating the order status until the order is complete (fulfilled and invoiced).

* * *

[**Acknowledgement**](/kb/logicbroker/360022058351-Acknowledgement-Specification?hsLang=en)

This document is used to accept/acknowledge, cancel, or back-order any items from the order.

* * *

[**Shipment**](/kb/logicbroker/360022058371-Shipment-Specifications?hsLang=en)

This document is used to notify your partner of all shipped items that were ordered. Shipments will contain containerized data (number of boxes and dimensions) and tracking numbers associated with them. 

* * *

[**Invoice**](/kb/logicbroker/360022058331-Invoice-Specification?hsLang=en)

This document is used to provide your partner with billing details related to their order. It will contain all item pricing for goods fulfilled and other related payment data.

* * *

[**Return**](/kb/logicbroker/360021911472-Return-Specification?hsLang=en)

This document is sent to your partner when a return is physically received on an order previously fulfilled. It will typically provide data on which products were received, why it was returned, and then a credit can be issued. 

* * *

[**Inventory**](/kb/logicbroker/360022025472-Inventory-Specification?hsLang=en)

Inventory documents contain all quantities and cost available for sale to your channels. They are transmitted per partner or can be broadcast using one feed to all connected channels. 

##### Integration Options

**Portal**

This is the easiest way to begin processing documents with your channel. Using the portal you can manually manage all orders, acknowledge, ship, invoice and update inventory. A user account will be provisioned and will be available for all integration options.

* * *

**EDI**

EDI (electronic data interchange), can be implemented to receive orders (850), send acknowledgements (855), shipments (856), invoices (810), and inventory (846) as an automated approach. We offer standard EDI specifications to follow or can provide custom specs to be mapped. Our EDI connection options include AS2, SFTP/FTP, or VAN. 

* * *

**API**

Logicbroker offers a full REST API to all data on our platform. All document types can be easily integrated with your system with some development effort. We offer JSON, XML, or CSV as different payload types. For more details visit our [developer documentation](https://dev.logicbroker.com) and [API reference](https://commerceAPI.io).

* * *

**JSON**

You can send and receive documents using our standard JSON formats. You can connect using SFTP/FTP or REST API right our of the box with minimal configuration.

* * *

**XML**

Documents can be sent and received using our standard XML formats or you can provide a custom XML specification to be mapped in our system. You can connect using SFTP/FTP or REST API.

* * *

**CSV/XLSX**

Documents can be sent and received using standard CSV or XLSX formats. Custom CSV/XLSX files can be used to create a mapping to our system. You can connect using SFTP/FTP, REST API, or bulk upload through the portal.

##### Processing Workflow

All documents in the Logicbroker system are processed based on [status](/kb/logicbroker/360022067771-Document-Statuses?hsLang=en). Workflows are configured to send documents to your partners or integrated systems. Statuses on your documents will indicate what action you need to take next to process your documents. 

**For example:**

The **Ready to Acknowledge** status on an order will indicate an acknowledgement should be sent. **Ready to Ship** will show an order is awaiting shipment, **Ready to Invoice** will show an order is waiting for an invoice, etc.

Statuses will change as documents are received on linked orders, indicating the successful transmission to your systems and partners. Statuses can be updated on your documents to resend or re-transmit to your system or partners.

####  🗒️Note:

Logicbroker can customize your workflow to connect to integrated systems, trigger webhooks, or send documents to custom endpoints/locations. We can integrate with any customized business workflow. [Contact us](https://www.logicbroker.com/company/contact-us/) for more information.

As we process your documents, all information is validated through our validation engine to ensure compliant information is transmitted through to you, your partners and your systems. Any failed transmissions will trigger email notifications to your account and configured users. 

#### ✨ __ Tip:

The Logicbroker platform also uses duplicate checking to make sure you are not processing duplicate documents. If a document is received with a duplicate ID, header, and item information we will prevent the document from transmitting.