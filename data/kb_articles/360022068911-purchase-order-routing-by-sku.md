---
title: "Purchase Order Routing by SKU"
url: "https://support.logicbroker.com/kb/logicbroker/360022068911-purchase-order-routing-by-sku"
category: "Platform"
---

March 3, 2026

# Purchase Order Routing by SKU

## 

**SKU Based Vendor Sourcing (Purchase Orders)**

SKU based vendor sourcing is a function of *Logicbroker Workflows*. When sending purchase orders to Logicbroker to be sourced, you have the option for Logicbroker to source the orders based on the SKU tied to a specific supplier. Logicbroker will look at each item on the sales order and identify which suppliers carry the product. Once determined, we will create a purchase order that goes out to that specific supplier to have it fulfilled.

**Setup Process**

  1. Confirm you want Logicbroker to do the sourcing
  2. Logicbroker will work with you on setting up a matching file for each of your suppliers and the SKUs that would be sourced to them
  3. Send Logicbroker a sales order to be sourced by SKU