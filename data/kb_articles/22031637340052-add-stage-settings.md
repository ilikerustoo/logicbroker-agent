---
title: "Add stage settings"
url: "https://support.logicbroker.com/kb/logicbroker/22031637340052-add-stage-settings"
category: "Supplier Onboarding"
---

March 9, 2026

# Add stage settings

## 

**Note** : You will need to reapply these settings once you move to the production portal as settings do not carry over from stage to production. 

### 

### **Send packing slip sample for approval (required for some API/EDI suppliers)**

_*This step is required for some**API** and **EDI** suppliers_

API and EDI suppliers have 2 options for handling packing slips:

If you do not plan on using Logicbroker's You can set up default or partner-specific payment terms. For more information, see [**Document Settings**](http://help.logicbroker.com/hc/en-us/articles/8058922786836-Document-Settings?hsLang=en#h_01G8DY65DC17EJWXFY5J2Q65CE). 

  1. **Use Logicbroker generated packing slips** – these are retailer-branded and are available in the portal. You will need to log into the portal to download/print. You may do this on individual orders or do this in bulk. For more information, see [**Shipments** ](http://help.logicbroker.com/hc/en-us/articles/7973910593940-Shipments?hsLang=en)> **Download Packing Slips**
  2. **Create your own** – review your retailer's packing slip specs to map your own slip in your system. If you do this, send a sample to your retailer for approval



### **Set up your connection (API/EDI/Shopify suppliers)**

_*This step is required for**API, EDI** and **Shopify** suppliers _

  * **API Suppliers** : Generate a stage API key from the [**API Authentication**](https://stageportal.logicbroker.com/profile/api-authentication) page
  * **EDI Suppliers:** Add your stage EDI connection from the [**EDI Connection**](https://stageportal.logicbroker.com/settings/edi) page
  * **Shopify Suppliers:** Add your stage Shopify connection from the [**Connections**](https://stageportal.logicbroker.com/connections) page 
  * **ShipStation Suppliers** : Add your stage Shopify connection from the [**Connections**](https://stageportal.logicbroker.com/connections) page 



### **Set up shipping SCAC codes (optional)**

_*This step is optional for**API** and **EDI** suppliers_

If your system uses a different code than the one listed under Standard Code, you will need to add a Custom Code so our system can match your Custom Code to our Standard Code. Our system will translate your custom code to our standard code on all orders and return documents. If a code is received that is not mapped, you may receive an error and your document may fail. For more information, see [**Shipment Options**](/kb/logicbroker/360022068771-Shipment-Options?hsLang=en).

  1. In the Logicbroker portal, go to **Settings** > [**Shipment Options**](https://stageportal.logicbroker.com/shipment-options) > **Ship Method Mappings**
  2. You will see a list of all the ship methods that all your retailers accept (to see partner-specific ship methods, scroll down to **Partner Ship Method Mappings**).
  3. If the **Standard Code** column lists a code different than the one in your system, click on **Edit** > add your **Custom Code** to map a **Custom Code** for our system to recognize the code you will be sending



### **Turn on auto-invoicing (Shopify suppliers)**

_*This step is required for**Shopify** suppliers_

If your retailer requires invoices for all shipped items, you can either [**manually create invoices**](http://help.logicbroker.com/hc/en-us/articles/7976629028884-Invoices?hsLang=en) in the portal or turn on auto-invoicing for Logicbroker to automatically create invoices on your behalf.

  1. In the Logicbroker portal, go to **Settings** > **Account Information > **[**Shipment Settings**](https://stageportal.logicbroker.com/settings/default-shipment-properties)
  2. Turn on the **Create Invoice from Shipment** setting



### **Set up default addresses (optional)**

You can set up default or partner-specific remittance, ship from and return addresses. For more information, see [**Document Settings**](/kb/logicbroker/8058922786836-Document-Settings#h_01G8DY65DC17EJWXFY5J2Q65CE). 

  1. In the Logicbroker portal, go to **Settings** > [**Account Information**](https://stageportal.logicbroker.com/profile/account-information)
  2. Add default addresses for each



### 

### **Set up acknowledgement setting (optional)**

You can set up default or partner-specific acknowledgment settings for default days to ship, exclude weekends and cancellation reason. For more information, see [**Document Settings**](/kb/logicbroker/8058922786836-Document-Settings#h_01G8DY65DC17EJWXFY5J2Q65CE). 

  1. In the Logicbroker portal, go to **Settings** > **Account Information** > [**Acknowledgement Settings**](https://stageportal.logicbroker.com/settings/default-ack-properties)
  2. Add acknowledgement settings



### **Set up return reasons (optional)**

You can set up default or partner-specific return reasons. For more information, see [**Document Settings**](/kb/logicbroker/8058922786836-Document-Settings#h_01G8DY65DC17EJWXFY5J2Q65CE). 

  1. In the Logicbroker portal, go to **Settings** > **Account Information > **[**Return Reasons**](https://stageportal.logicbroker.com/settings/default-return-properties)
  2. Add a return reason



****

### **Set up shipment setting (optional)**

You can set up default or partner-specific shipment settings. For more information, see [**Document Settings**](http://help.logicbroker.com/hc/en-us/articles/8058922786836-Document-Settings?hsLang=en#h_01G8DY65DC17EJWXFY5J2Q65CE). 

  1. In the Logicbroker portal, go to **Settings** > **Account Information > **[**Shipment Settings**](https://stageportal.logicbroker.com/settings/default-shipment-properties)
  2. Add shipment settings: 
     * **UCC128 (GS1) Company ID** – if you are working with a retailer that requires GS1 labels, this is where you will enter in your UCC128 Company ID used to generate the labels - these are normally required for bulk and replenishment orders. For more information on GS1 Labels and UCC 128 Company IDs, see [**here**](https://www.gs1-128.info/sscc-18/). 
     * **Copy Ship Method From Order** – toggle this on if you want ship methods on shipments to be defaulted to what the retailer sent on the order Please note: you are still required to ship orders using the retailer-requested ship method **Note** : This setting is for Logicbroker customers
     * **Create Invoice From Shipment** – toggle this on if you want complete shipments to trigger an invoice document to be created and sent out to the retailer on your behalf Please note: invoices will be populated using a random invoice number **Note** : This setting is for Logicbroker customers



### **Set up notifications (optional)**

You can customize email notifications. Notifications need to be set up on an individual user basis. If you turn on a notification, it will **not** be sent to all users in your company. For more information, see [**Notification Explanations**](http://help.logicbroker.com/hc/en-us/articles/360022057611?hsLang=en#sidenav-article-360022057591).

  1. In the Logicbroker portal, go to **Settings** > [**Notifications**](https://stageportal.logicbroker.com/profile/notifications)
  2. Toggle on the notifications you wish to receive through email
  3. **Save**