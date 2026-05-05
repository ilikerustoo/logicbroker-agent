---
title: "Routing Orders to Multiple Companies"
url: "https://support.logicbroker.com/kb/logicbroker/360022068971-routing-orders-to-multiple-companies"
category: "Platform"
---

March 3, 2026

# Routing Orders to Multiple Companies

## 

**Route orders to Multiple Companies**

Routing orders to Multiple Companies is a function of *Logicbroker workflows*. This allows order data (can be used for other documents as well) to be transferred between more than 2 companies. This is useful for a 3PL-type flow, or if there is another system that needs to receive order/transaction data, after it has already been communicated between 2 different companies. Once an order is received, the workflow triggers based on the document sender and receiver, and exports all the document's data to an additional company and/or entity.

**Example of Use**

You are a supplier who uses a 3PL for order fulfillment. Because you and your 3PL have their own separate ERP systems, you will need to receive your order data in one format, and your 3PL will need to receive it in their own format. This workflow will be setup so that you receive the document data as you need, and the 3PL will then also receive the same information in their specified format.

**Setup Process:**

  1. Identify need for a 3rd party to receive order lifecycle documents
  2. Indicate to Logicbroker which company/entity will need to receive documents
  3. Determine which documents you will need, as well as the third party
  4. Logicbroker will setup the workflow according to the stakeholders’ requirements