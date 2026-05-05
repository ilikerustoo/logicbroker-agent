---
title: "Release Notes Through 2/1/2021"
url: "https://support.logicbroker.com/kb/logicbroker/360055536192-release-notes-through-2-1-2021"
category: "Logicbroker Updates"
---

March 3, 2026

# Release Notes Through 2/1/2021

## 

#### Portal Updates:

  * **Email fields** are editable on **failed** orders.
  * A simplified **cost-based sourcing** algorithm is now live.
  * **Failed document events** are visible in bulk using the **Failed Document Summary** under the **Reports** section.
  * Connector functionality is displayed on the **Connections** page.
  * Failed document events are consolidated into a single summary on the **Failed Documents** page within the **Reporting** function.
  * Original carrier and service level codes are stored for **ship method mappings**. 



#### Connector Updates:

  * **ShipStation:** Shipments can be configured to pull fulfillments into the Logicbroker Portal from ShipStation.
  * **Shopify** : Customers can be notified when orders (placed through API) are shipped.
  * **Magento** : New multi-source Inventory options are available. 
    * Functionalities include: ignore item sources, put all items under a single source, use of vendor number from inventory as source code, use of supplier account number as source code.
    * Ability to specify source code on shipments, if this is not provided the default source will be used.

    * Only orders less than 30 days old will be sent.