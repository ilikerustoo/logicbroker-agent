---
title: "Purchase Order Creation/Routing by Cost"
url: "https://support.logicbroker.com/kb/logicbroker/360022068951-purchase-order-creation-routing-by-cost"
category: "Platform"
---

March 3, 2026

# Purchase Order Creation/Routing by Cost

## 

**Cost Based Vendor Sourcing (Purchase Orders)**

Cost based vendor sourcing is a function of *Logicbroker Workflows*. When sending purchase orders to Logicbroker to be sourced, you have the option for Logicbroker to source the orders based on supplier and cost. Logicbroker will look at each item on the sales order and identify which suppliers carry the product. Once identified, Logicbroker will check which of those suppliers have the product available (checking against their latest inventory feed). Once all possible suppliers have been identified, Logicbroker will compare costs as well as "compactness" * for all available vendors and send the appropriate quantities on a purchase order to the supplier(s) with the most competitive pricing, as well as creating the most compact score.

* Compactness is scored using the following data points

  * Quantity
  * Cost
  * Fewest Suppliers
  * Highest "Score" - Score is based on the Logicbroker algorithm



**Example of Use**

You are a retailer who offers a product sold by multiple distributors. You are unsure which supplier/distributor currently has the best pricing. You enable cost based sourcing to automatically send purchase orders for that item to the supplier(s) with the amount on hand, and the lowest price. Logicbroker will then create purchase orders for each supplier as needed.

**Setup Process**

  1. Confirm you want to setup cost based sourcing
  2. Logicbroker will setup cost based sourcing on your account
  3. Send Logicbroker a sales order to be sourced by cost