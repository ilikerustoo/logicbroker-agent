---
title: "Step 3: Setting Up Suppliers/Warehouses and Products"
url: "https://support.logicbroker.com/kb/logicbroker/360021847652-step-3-setting-up-suppliers-warehouses-and-products"
category: "Retailer Onboarding"
---

March 3, 2026

# Step 3: Setting Up Suppliers/Warehouses and Products

## 

To begin testing and ultimately launching with your trading partners (drop ship suppliers/3PL fulfillments), you need to set them up as suppliers with Logicbroker.

You can add new Suppliers/Warehouses by emailing [support@logicbroker.com](mailto:support@logicbroker.com) with the following information:

  * Supplier Name
  * Supplier Address, City, State & Zip
  * Contact Name
  * Contact Phone
  * Contact Email



The information will be reviewed with our internal team to see if we already have an integration, or if a new integration will need to be set up. Once the trading partners are set up and approved, they will get propagated to Logicbroker's test environment and configured for both testing and live document exchange. Additionally, the suppliers will appear on the **Suppliers** page of the Logicbroker portal.

On the Suppliers page of the Logicbroker portal you can see the Company ID; this will be used for your ReceiverCompanyId parameter when sending documents (Orders) and SenderCompanyId when receiving documents (Acknowledgments, Shipments, and Invoices). This is important when using the XML, JSON, and EDI formats. If you are creating sales orders in Logicbroker then this field will not be required.

####  __ Tip:

To learn more about the supplier onboarding process and how communication is sent to all of your suppliers see [this article](http://help.logicbroker.com/hc/en-us/articles/360022058111?hsLang=en).

## Inventory/Product Setup

When preparing to integrate with a new supplier and inventory updates will be provided, it is recommended to setup your supplier's products beforehand. This will provide a definitive list requiring your supplier to update the list of products that were setup. As this is not mandatory the setup process can be managed in 2 ways; having the retailer setup products or allowing the supplier to setup their own (No Setup).

### Retailer Sets Up Products

In this scenario, the retailer sets up a **MerchantSKU** to **SupplierSKU** link for each product. The **MerchantSKU** will not change and will require that the supplier updates all products using the matching **SupplierSKU** to update that product. Non-matched products will not be sent to your account.

Typically the **MerchantSKU** will be different from **SupplierSKU** , but can be the same value if needed.

####  __ Tip:

For full instructions on setting up inventory for your suppliers in the portal see [this article](http://help.logicbroker.com/hc/en-us/articles/360025660832?hsLang=en).

### No Setup

In this scenario the supplier can submit any **SupplierSKU** with their inventory updates and the **MerchantSKU** will automatically default to the same value. This will allow all products to send to your account, requiring your system to filter out any mismatched products. In addition this will require your system to have a match for the **SupplierSKU** provided as the **MerchantSKU** and **SupplierSKU** will be the same.

To enable this setup process, under **Products** > **Inventory Feeds** you can select your partner and under **Feed Settings** enable **Auto match**

[](https://support.logicbroker.com/hubfs/Knowledge%20Base%20Import/Products_Inventory_FeedSettings-3.png?hsLang=en)

Note this setting is setup per partnership; so if this is required for all of your suppliers, the **Auto match** flag must be enabled for all.