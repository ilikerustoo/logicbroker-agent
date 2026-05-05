---
title: "Product Content (Product Feeds)"
url: "https://support.logicbroker.com/kb/logicbroker/360023030132-product-content-product-feeds"
category: "Retailer Onboarding"
---

March 10, 2026

# Product Content (Product Feeds)

## 

Logicbroker has the ability to collect product content from all of your suppliers, validate formats and integrate with your PIM*, CMS**, DAM***, or eCommerce systems. This allows you to collect product data from 100s of channels, allowing your suppliers to upload content in your format and verify that their content is always compliant with your requirements. Below is a step by step process for getting your product content integrated.

*Product Information Management, **Content Management System, ***Digital Asset Management

#### ✨Tip:

To learn more about uploading product content see [this article](/kb/logicbroker//360021857852-Product-Feeds?hsLang=en).

##### Setting Up Format

First we need to determine the data required to receive from your suppliers. This can include fields like image URLs, product SKUs, descriptions, ingredients, etc. The format templates created for your suppliers will always use a CSV format. All header columns can be customized to contain the following field types:

Field Type | Description  
---|---  
**String** |  Standard collection of characters.  
**Integer** |  Whole number field.  
**Decimal** |  e.g. 3.14  
**Image URL** |  Used to transmit images for the product using URL. Setting this type for the field will show the product in the portal Product Search page with the image of the provided URL.  
**Name** |  The Name type will show the product name in the portal's Product Search page.  
**Category** |  Indicates if the field is a category which would be used to create separate templates for each option.  
  
By default you will be able to receive all of your feeds in this format as well using an SFTP/FTP connection. All field column names cannot contain any special characters, such as forward slash (/), backslash (\\), number sign (#), question mark (?), control characters, dashes (-) and spaces.

#### 🗒️Note:

If you are integrating using a custom API, Logicbroker can connect your content to your system converting the custom CSV template into the required format needed to integrate.

##### Required Rules and Validation

Once your CSV format is created with all columns, the next step would be setting up the rules for different templates per product category and validation for all your fields. When a feed is submitted, we will not only check the format of the field, but can also validate specific data setup.

Below is a list of rules we can setup on your feed; a rule is a parameter setup to check against the field value that is being submitted. The rules can also include conditions, where they will only run validation against if they meet that condition. The condition can relate to another field in the feed or refer to the same field. Each field can have an unlimited number of rules and conditions.

Rule Type | Description  
---|---  
**Required** |  A rule that will make the field required. Usually used with a condition looking up Category. For example, you can add a condition to always include "Size" when the Category is "Shoe" In addition, by setting this condition the supplier will have the ability to download templates for each category including only the required fields.  
**Equals** |  Used to check the value submitted in the field equals the parameter set. If the field does not match the product will fail validation and show as non-compliant.  
**Not Equals** |  Used to check the value does not equal the parameter set. If the field matches the parameter the product will fail validation and show as non-compliant.  
**In List** |  Will check the value submitted against an array of values. The array can contain an unlimited number of values to check against. If the value is not in the list the product will be marked as non-compliant.  
**Matches Expression** |  A regular expression can be written to check against the value submitted. This can be an exression to verify a valid UPC is being sent or only alpha numeric characters provided.  
**Length Equals** |  Check the number of characters are provided in the field and compares against the parameter set. For example if 10 is set the value provided must contain 10 characters.  
**Length Less Than** |  Checks the number of characters provided in the field and if the length is not less than the parameter setup, the product willl be marked as non-compliant.  
  
##### Integrating Product Feeds

Once you have your format and validation rules setup you can setup an integration to receive your content feeds. Out-of-the-Box SFTP/FTP integration is offered as an integration option.

Using your Logicbroker credentials and logging into your SFTP/FTP site, you will see the **/Product** directory. Go there and into the **/Product/ <PartnerAccount>/Inbound** directory, this is where all files are sent to, from your suppliers. All files here will have passed validation setup and have been verified to process successfully; suppliers cannot send their feeds until all products have passed validation. To learn more about the SFTP/FTP directories, see [this article](/kb/logicbroker//360022067631-SFTP-FTP?hsLang=en). To learn more about the process for managing compliant and non-compliant products in the portal, see [this article.](/kb/logicbroker//360021857852-Product-Feeds?hsLang=en)

#### 🗒️Note:

We also have the ability to connect your product content to any API or system. For more information on available system connectors and creating a custom connection [contact us](https://www.logicbroker.com/company/contact-us/).