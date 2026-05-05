---
title: "Product Feed Rules"
url: "https://support.logicbroker.com/kb/logicbroker/7903827173780-product-feed-rules"
category: "Platform"
---

March 13, 2026

# Product Feed Rules

## 

**Audience :** Retailer customers

In this article, you will find information related to rules that can be applied to product feeds. The sections within this article are outlined below:

  * Overview
  * Navigating to Product Feed Rules 
  * Product Feed Rules Defined
  * How to Apply a Rule
  * Related Content



##### Overview 

This functionality is available for **retailers **to set rules that will apply to all product feeds that are received from partners. The **rules **are applied **before **the items are uploaded to the retailer’s feed.

Rules help retailers transform data that is being received. Rules can be applied to combine fields, add default fields, and concatenate fields.

##### Navigating to Product Feed Rules in the Portal

Under the Feed Specification of the Product Feeds page, click on the rules button.

You will then see a view similar to the one shown below.

##### Definitions

**At a Glance**

  * **Order **– this is the sequence in which the rules are applied.
  * **Field **– the retailer’s product feeds fields.
  * **Maps From** – this is the rule (transformation) you have created for the field.
  * **Condition** – when a condition is set, rules will only run if the condition is met. For example, if the type is equal to digital, then the rule will run.



**Actions**

  * **Add Rule** – this provides the ability to configure rules for your product feed
  * **Save to File** – by saving your rules, you are able to easily transfer your configurations from Stage to Production. By clicking this button, a file is generated with these configurations.
  * **Load from File** – by saving the configurations to the file, you are able to import the configurations into different environments by clicking on the **Load from File** button and upload the file.
  * **Save **– this captures any new rules or changes you have made for your product feeds. It is important to always be mindful of saving because if you do leave the page without clicking this, your work will be lost.
  * **Edit **\- this appears on each of the rules that have been created for your feed. This captures any new rules or changes you have made for your product feeds
  * **Add **\- this appears on each of the rules that have been created for your feed and will pull the attribute from that rule to create a new rule so you will only need to apply the field expression
  * **Remove **– this appears on each of the rules that have been created for your feed and is used to take away any rules you no longer want to apply.



##### How to Apply a Rule:

  1. Click on the **Add Rule**
  2. Select an **Attribute** from the field’s drop-down menu. These attributes are the retailer’s attributes.
  3. Add the **Source Expression Field**. This is the transformation you would like to make to your data. The value you are looking to how you want the data to appear in the product feed file. For example, if you are selling clothing and wanted to easily distinguish that the items are women’s clothing you can add this before the product name. The expression would be “Women’s” + Name, as shown in the image below. Be sure to enclose the constant values in quotes. Once complete, click **continue**. 
  4. Once your rules are added be sure to click the **Save **button on the top of the screen.
  5. If you have multiple rules configured, you are able to organize them in the order you would like to have them applied. Hover over the six dots and drag the rules into the preferred order.  
Once complete, be sure to click **Save**.
  6. When a new product feed is received, open the file and you will see your transformations have appeared in the file.