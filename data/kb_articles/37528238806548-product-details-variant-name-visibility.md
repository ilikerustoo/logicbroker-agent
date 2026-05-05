---
title: "Product Details & Variant Name Visibility"
url: "https://support.logicbroker.com/kb/logicbroker/37528238806548-product-details-variant-name-visibility"
category: "Platform"
---

March 3, 2026

# Product Details & Variant Name Visibility

## 

### **Demo Video**

### ** **

### **Audience**

This article applies to all **retailers using Logicbroker’s Product Onboarding Center (POC) to view or manage product data** , regardless of connection type (e.g., portal, API, Shopify, or EDI). It also applies to **suppliers managing product and variant data through the Logicbroker portal or other integration methods**.

_**Please note:** These changes **do not yet** apply to users leveraging the **supplier flow syndication** functionality._

### **Overview**

**T his demo highlights recent updates to Logicbroker’s Product Onboarding Center (POC), aimed at improving usability, transparency, and efficiency for users managing product data. **

### **Key Updates**

  1. Variant Name Visibility
  2. Enhanced Variant Details Page
  3. Clear Distinction Between Product-Level & Variant-Level Fields
  4. Changelog Enhancements
  5. Improved Data Navigation
  6. Varying Attributes Clearly Marked
  7. Quick Variant Switching



### **Key Clarifications**

**No Impact on existing workflows**

No action is required from retailers or suppliers.

  * **CSV structures and existing workflows remain unchanged**
  * The update is **strictly visual/UI-related** , designed to make the POC experience more intuitive and reduce ambiguity when viewing variant-level details.



**Variant Name Logic**

The variant name displayed in the line-item view is tied directly to the **Variant Name attribute** in your taxonomy.

  * If this attribute is not present or in use within your taxonomy, the variant name **will not appear** in the UI.
  * This does **not** impact how your product data is stored or processed — it only affects **how data is displayed** within the portal to help stage products for your next system.
  * The Variant Name **will not** render in the line-item view **until the variant has been updated**.



### **1\. Variant Name Visibility**

  * **Feature:** The variant name is now included in the line-item view.
  * **Format:** Displayed as Product Name | Variant Name.
  * **Why it matters:** Helps users distinguish between variants when SKUs are non-intuitive or variant images are missing. By displaying this information on the main table, users are able to quickly take action and reduce some of the manual touchpoints.



### **2\. Enhanced Variant Details Page**

  * **Variant Summary Card:** At the top right, a new UI card displays selected option values (e.g., Gray, Medium, Crew).
  * **Supports Friendly Name Mapping:** Users can define friendly names for their attributes like "Color", "Size", "Neckline" for options. Attribute Friendly Name configurations can be found in the retailer’s Taxonomy settings



### **3\. Clear Distinction Between Product-Level & Variant-Level Fields**

  * **Variant-Level:** Fields marked with the lavender “Variant Field” pill icon (e.g., barcode, cost, price) affect only the selected variant.
  * **Product-Level:** Changes (e.g., product name) apply to all variants and are reflected globally.



  * **Managing Variations  
**
    * Variant-level attributes can still be reconfigured using the **Manage Variations** interface located beneath your list of variants.
    * Any attributes not included in the variant-level configuration will be treated as product-level attributes.
    * Attributes selected in the **Varies By** list will define which characteristics differentiate the product variants.



_**Note:** If you're using Shopify, you are limited to a maximum of **125 variants per product** and **3 Varies By attributes**._

__

### **4\. Changelog Enhancements**

  * **Automatic Scope:** Product-level updates auto-apply across all variants (no checkbox needed).
  * **Variant-level changes:** Can be saved independently or optionally copied to others.
  * **Example Scenario:**



****

  * In the example shown above, I updated one of my variants so that the product name reads **"Sailor T-Shirt test Updated product Name"** , and I adjusted the **price** and **compare-at-price** attributes to **$120** and **$180** , respectively.
  * Because the **product name** is a product-level attribute, this change appears in the **product-level change log** on the left-hand side of the modal. As a product-level attribute, the updated name is automatically applied to **all variants** under that product. 
  * In contrast, the **price** and **compare-at-price** are variant-level attributes, so these changes appear in the **variant-level change log** on the right-hand side of the modal. Since variant-level attributes are specific to each variant, the updates apply **only to the variant being edited**. 
  * If you'd like to apply a variant-level update (such as price) across **all variants** of the product, you can use the checkbox located below the variant-level change log. In this example, I chose **not** to apply the pricing updates to other variants, so I left the checkbox **unchecked**.



### **5\. Improved Data Navigation**

  * **Legacy UI Limitation:** Users had to scroll horizontally to see variant data.
  * **New UI:** Variant-specific details now appear in a fixed card layout, making review and edits easier.



**Before**

**After**

### 

### **6\. Varying Attributes Clearly Marked**

  * **"Varies By" Tags** highlight attributes that define variant structure (e.g., color, size, neckline) are now visually tagged with the green “Varies By” pill. 
  * **Purpose:** Helps users quickly identify what differentiates each variant.



### **7\. Quick Variant Switching**

  * **New List View:** A list of all variants for a product is now directly accessible from the detail page.
  * **Seamless Navigation:** Users can switch between variants without reloading the page