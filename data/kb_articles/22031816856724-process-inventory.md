---
title: "Process Inventory"
url: "https://support.logicbroker.com/kb/logicbroker/22031816856724-process-inventory"
category: "Supplier Onboarding"
---

March 3, 2026

# Process Inventory

## 

**Note** : You will need to upload/send a live inventory feed once you move to the production portal as feeds do not carry over from stage to production. 

###  **Portal, EDI, API and ShipStation Suppliers**

  * Review your retailer's inventory requirements: 
    * **For Portal and API Suppliers** : from the [**Document Standards**](https://stageportal.logicbroker.com/document-standards?type=Inventory)**** page in the portal.   
  
****  

    * **For EDI Suppliers:** from the [**EDI Connections**](https://stageportal.logicbroker.com/settings/edi) page.  
  
  

  * Create your inventory file 
    * **Portal Suppliers:** Go to **Import** > **Templates** > download the **Inventory Feed Template** > fill it out  
  

    * **API, EDI Suppliers:** Your development and EDI teams should work on mapping all API/EDI specs and getting the file ready to send from your system.   
  

  * Upload or send your inventory file
    * **Portal Suppliers** : Upload your template file into the portal from the [**Inventory**](https://stageportal.logicbroker.com/advanced-product-management) page >**Import** > **Upload Files** > **Supplier Feed**. **Note** : Excel uploads are preferred since CSV may cause scientific notation errors
    * **API, EDI Suppliers** : Send the inventory file through your established connection. Ensure you are sending it to the correct environment (if you are testing, please send inventory to our stage environment).
  * Confirm your inventory file was uploaded/send successfully: In the portal, from the [**Inventory**](https://stageportal.logicbroker.com/advanced-product-management) page, go to **Events** > look for the **Inventory Imported** event to ensure your file was uploaded successfully. Review any errors and reupload/resend if necessary. 



### **Shopify Suppliers**

  * In Shopify, make sure all the products you want to share with your partner are in an **Active status** , have a **unique SKU** and are **tagged with 'Logicbroker'**



  * Logicbroker will automatically pull in inventory for the products that meet the criteria into Logicbroker every 30 minutes. Once the job runs, we will store the inventory data in Logicbroker and send it to your partner. 



### **Squarespace Suppliers**

  * In Squarespace, make sure all the products you want to share with your partner are in a **Public status**. 



  * Logicbroker will automatically pull in all inventory for the products that meet the criteria into Logicbroker every 30 minutes. Once the job runs, we will store the inventory data in Logicbroker and send it to your partner.