---
title: "Process Products (Product Onboarding Center)"
url: "https://support.logicbroker.com/kb/logicbroker/27789943193236-process-products-product-onboarding-center"
category: "Supplier Onboarding"
---

March 3, 2026

# Process Products (Product Onboarding Center)

## 

**Note** : You will need to upload/send a live product file once you move to the production portal as feeds do not carry over from stage to production. 

For more information on the page, permissions, data flow, etc., see [**Product Onboarding Center**](http://help.logicbroker.com/hc/en-us/articles/21106796071956-Product-Onboarding-Center?hsLang=en)**.**

### **Portal, EDI, API and ShipStation Suppliers**

  * Download a template: Go to the **Product Onboarding Center** > [**Import**](https://stageportal.logicbroker.com/productonboardingcenter/import)**** page > select your retailer > '**Download template** '



  * Upload or send your product feed 
    * **Through the portal** : Upload your template file into the portal from the **Product Onboarding Center** > [**Import**](https://stageportal.logicbroker.com/productonboardingcenter/import)**** page
    * **Through the API** : Use this endpoint to send a product feed: [**POST /api/v2/ProductOnboardingCenter/Products**](https://stage.commerceapi.io/swagger/ui/index#!/ProductOnboardingCenter/ProductOnboardingCenter_CreateProduct)
  * Confirm you product file was uploaded successfully: In the portal, **Product Onboarding Center** , go to [**My Catalog**](https://stageportal.logicbroker.com/productonboardingcenter/catalog?catalog=mycatalog) > review the products that were added.



### 

### **Shopify Suppliers**

  * In Shopify, make sure all the products you want to share with your partner are in an **Active status** , have a **unique SKU** and are **tagged with 'Logicbroker'**



  * Logicbroker will automatically pull in all products that meet the criteria into Logicbroker everyday at 12am EST. Once the job runs, we will store the product data in Logicbroker and send it to your partner. 



### **Squarespace Suppliers**

  * In Squarespace, make sure all the products you want to share with your partner are in a **Public status**. 



  * Logicbroker will automatically pull in all products that meet the criteria into Logicbroker everyday at 12am EST. Once the job runs, we will store the product data in Logicbroker and send it to your partner.