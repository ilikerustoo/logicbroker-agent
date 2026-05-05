---
title: "Auto-populating Address Information from Address Code"
url: "https://support.logicbroker.com/kb/logicbroker/360021858032-auto-populating-address-information-from-address-code"
category: "Platform"
---

March 3, 2026

# Auto-populating Address Information from Address Code

## 

**Auto Populate Address Information from Address Code**

Logicbroker has the ability to populate address information based on an address code field received on orders. Retailers may send a code for a distribution center or store for Ship-to-store orders. In this case, Logicbroker manages these codes and their respective addresses. When the order passes through Logicbroker to the suppliers, all address fields (address line 1, address line 2, city, state, zip, etc.) will be populated.

**Example of Use**

You are connected to a retailer that sends address codes instead of full addresses via EDI. Logicbroker will know what specific address this code relates to, and will populate the address information based on the code received. If the retailer sends a code of “A9856” to represent one of their stores, Logicbroker will map this store code to the appropriate address so that the vendor community receives the entire address instead of only the address code.

_Logicbroker uses lookup tables to relate an address code to its appropriate address_

__

**Setup Process**

  1. Logicbroker manages address codes directly from the retailers
  2. If you receive an order with no address lookup, reach out to Logicbroker to have them update their lookup so all address codes can be added