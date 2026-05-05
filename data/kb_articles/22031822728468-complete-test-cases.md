---
title: "Complete test cases"
url: "https://support.logicbroker.com/kb/logicbroker/22031822728468-complete-test-cases"
category: "Supplier Onboarding"
---

March 3, 2026

# Complete test cases

## 

### **Review your partner's document specifications**

**Portal, API, Shopify and ShipStation Suppliers** : Review your partner's inventory requirements from the [**Document Standards**](https://stageportal.logicbroker.com/document-standards?type=Inventory)**** page in the portal. 

**EDI Suppliers** : Review your partner's document specifications from the [**EDI Connections**](https://stageportal.logicbroker.com/settings/edi) page.

### 

### **Create test orders**

  1. In the Logicbroker portal, go to [**Testing**](https://stageportal.logicbroker.com/testing) > look for your retailer**** > **View**
  2. Review testing requirements for all test orders. For each of the test cases that apply to your business, click on **Create a New Test Order****Note****:** Once created, these orders will be visible in the [**Orders**](https://stageportal.logicbroker.com/order-management) page of the portal



  * **Portal Suppliers:** Review the order by clicking on the order number
  * **EDI/API Suppliers:** You should receive the order document in your system within a few minutes
  * **Shopify Suppliers** : You should receive the order in your Shopify account within a few minutes
  * **ShipStation Suppliers** : You should receive the order in your ShipStation account within a few minutes



**Note** : At any time, you can generate a new test order if you would like to start over, try again, etc. Just click on **Create A New Test Order**. Just note the previous test order will move to an **Ignored** status.

### **Tip!**

API and EDI suppliers can access raw formats of documents from the portal by opening up the document > **More Actions** > see available formats:   
  


### **Supplier - Complete Testing**

  * **Portal Suppliers** : In this step, you will process the required test cases in the portal by creating return documents directly in the portal. 
  * **EDI/API Suppliers** : In this step, you will process the required test cases in your system by sending return documents via your EDI/API connection. 
  * **Shopify Suppliers** : In this step, you will process the required test cases in Shopify by creating shipments/fulfilling orders. Cancellations should be created directly in Logicbroker.
  * **ShipStation Suppliers** : In this step, you will process the required test cases in ShipStation by creating shipments/fulfilling orders. Cancellations should be created directly in Logicbroker.



**Note** : You must complete testing using the connection method you plan on using in production. These are just test scenarios to ensure correct data flow, please do not ship any physical items out.