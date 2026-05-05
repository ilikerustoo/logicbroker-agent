---
title: "Carrying Settings from Stage to Production"
url: "https://support.logicbroker.com/kb/logicbroker/37713397369108-carrying-settings-from-stage-to-production"
category: "Supplier Onboarding"
---

March 3, 2026

# Carrying Settings from Stage to Production

## 

**Audience :** Suppliers

### **Overview**

Logicbroker now supports carrying settings configured in stage into production when suppliers go live for the first time. This is meant to reduce onboarding time and limit the settings suppliers need to reconfigure once they are live in the production portal. 

**Requirements**

  * Account must be a supplier account
  * Account must be going live for the first time (ex. if a supplier is live with partner A and while onboarding with partner B they set up new configurations in stage, these will not be carried over since the account is already live with another partner)



**Settings that will be carried over**

  * Account Information
  * Notifications
  * Inventory settings
  * Document settings
  * Shipment Options 
  * Shipment Boxes
  * EDI Custom Document settings (this does not include any other EDI settings - the connection itself will need to be re-established in production)



**Settings that will not be carried over**

  * Reports (Dashboard, Advanced Export, Scheduled Reports, etc.)
  * Connections (Shopify, EDI, API, etc.)
  * Product Onboarding Settings
  * Any settings on the retailer account including: 
    * Custom Lookup Table inputs
    * Global Inventory settings