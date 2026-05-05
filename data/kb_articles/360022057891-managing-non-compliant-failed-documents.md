---
title: "Managing Non-Compliant/Failed Documents"
url: "https://support.logicbroker.com/kb/logicbroker/360022057891-managing-non-compliant-failed-documents"
category: "Supplier Onboarding"
---

March 3, 2026

# Managing Non-Compliant/Failed Documents

## 

## **Get Alerted**

## When you are working with the Logicbroker portal you will want to ensure that you are subscribed to the Failed Document Report. This will send you an email alert each time a document is non-compliant or fails.

## **Take Action**

When an email is received you may take action by logging into the portal and identifying which documents have failed. This will be shown directly on the dashboard upon login and from there you may click on the boxes and drill down into the documents.

Once you have the list of documents you may click the view button. Within the document details, you will see an event at the top of the page. When you click on this event it will tell you the details around why the document failed.

After you have identified why the document failed, you can then resend the data if needed or address it with the sending party. If you have any questions you may also contact [support@logicbroker.com](mailto:support@logicbroker.com)

________________________________________________________________________________________________________________

### **Troubleshooting Production Errors**

See below for common production errors, causes and how to resolve them. 

#### **Failed to import order into NetSuite**

**Error** _**:**_ You have entered an Invalid Field Value ### for the following field: shipmethod 

**Description:** The Field Value is an internal ID for a shipping method in NetSuite. This error comes up when the SKU on the order is not properly configured for 3rd party shipping. 

**To Fix:** Set up the SKU on the order in NetSuite to be configured to 3rd party shipping. 

__

#### **EDI 856 rejected**

**Error****:** Logicbroker has encountered a failed functional acknowledgment from Houzz for document ###.

**Description:** This shipment was rejected by the receiving partner because they do not accept the carrier Airborne-WhiteGlove _  
  
_**Example**** _:_**_  
_**_  
_**_  
_**Find the error:** Open the failed shipment document > click on **More Actions** > **View EDI** > here you will see the 856 error: "WhiteGlove" exceeds the maximum length._  
__  
__  
  
_**To fix:**

  * From the failed shipment, copy the carrier  _Airborne-WhiteGlove_
  * In the portal, go to Settings > Shipment Options > Partner Ship Method Mappings > paste  _Airborne-WhiteGlove_ into the search bar
  * You will see only 3 retailers show up (Houzz is not one that accepts this code) and that the service level is WhiteGlove. This service level is what is failing on the 856 (because it exceeds 2 characters):



  * Type in  _Houzz_ into the search bar under Partner Ship Method Mappings
  * Here you will see all the carrier codes Houzz does accept, and you will see that the service levels are all 2 characters long



  * Copy the **description** of one of the carriers (the one that is most similar to the carrier the order was shipped with) and go back to the failed shipment
  * Once you are on the shipment document, click on **More Actions** > **Edit** > paste the new carrier > **Submit**