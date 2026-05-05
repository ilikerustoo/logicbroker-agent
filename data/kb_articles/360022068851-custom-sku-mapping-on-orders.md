---
title: "Custom SKU Mapping on Orders"
url: "https://support.logicbroker.com/kb/logicbroker/360022068851-custom-sku-mapping-on-orders"
category: "Platform"
---

March 3, 2026

# Custom SKU Mapping on Orders

## 

**Custom SKU mapping based on what the Supplier needs to receive:**

There are instances where the SKU value that the Retailer sends on the order does not match to the SKU value that Suppliers have in their system. Logicbroker has the ability via *Logicbroker Workflows* to do a lookup on the SKU that the Retailer provides on the order and then map it to the value needed to be sent to the end system. Logicbroker will save that incoming SKU and ensure that it is sent back to the Retailer as it was received.

**Setup Process**

  1. Confirm with Logicbroker that you will need this mapping set up
  2. Logicbroker will work with you on setting up a matching file that determines which SKU value you would like to receive
  3. Test the mapping as you go through the Retailer specific test cases