---
title: "API Authentication"
url: "https://support.logicbroker.com/kb/logicbroker/360022068791-api-authentication"
category: "Platform"
---

March 9, 2026

# API Authentication

## 

**Audience :** API users

In this article, you will find information related to **API Authentication Page** , connectivity and documentation. The sections within this article are outlined below:

  * Dev documentation
  * Set up your API connection



#### __ 🗒️Note:

The API Authentication page in the portal is only available to users with the**api/manage** permission. For more information on permissions, see [Manage Users](/kb/logicbroker/360021857352-Manage-Users?hsLang=en). 

### **Dev documentation**

  * Dev documentation to set up an API integration with our Rest API: <https://dev.logicbroker.com>
  * Stage Logicbroker API URL: <https://stage.commerceapi.io>
  * Production Logicbroker API URL: <https://commerceapi.io>



### **Set up your API connection**

  1. In the portal, navigate to **Settings** > **API Authentication  
**(**Stage link** : [API Authentication](https://stageportal.logicbroker.com/profile/api-authentication), **Production link** : [API Authentication](https://portal.logicbroker.com/profile/api-authentication/))

  2. Click on **Create Primary Key**

  3. If you are using a custom API requests and responses, you will need to provide those details either by emailing [support@logicbroker.com](mailto:support@logicbroker.com)




**Note** : If there is already a key generated, you should validate with all parties at your organization before generating a new key as it could break an existing connection. 

#### __ ✨Tip:

The Primary Key is generally for your internal use whereas the secondary key can be shared with your 3rd party development or external resources. Every request must have the API key as a URL query parameter (subscription-key).