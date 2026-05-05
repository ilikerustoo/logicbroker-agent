---
title: "Splitting Orders on Ship to Destination"
url: "https://support.logicbroker.com/kb/logicbroker/360022068891-splitting-orders-on-ship-to-destination"
category: "Platform"
---

March 3, 2026

# Splitting Orders on Ship to Destination

## 

**Orders for multiple Ship-to-locations**

When working with Replenishment integrations we find that it is common practice for Retailers to send an order that has multiple ship-to-locations. Logicbroker has the ability using *Logicbroker Workflows* to identify the different store/DC locations and generate a sub-PO for each so they can be easily identified and packaged by your warehouse. We also can do an address lookup, as many of these same retailers will send in an address code and expect you to map the correct ship-to address. We do this mapping for you, so you receive the ship-to information directly into your system with no lookup required. 

**Setup Process**

  1. When working with the Retailer, Logicbroker will determine if this splitting is required.
  2. Logicbroker will configure the workflows and address information accordingly.
  3. Test the mappings and ensure that everything is flowing into your system and back to the retailer as expected.