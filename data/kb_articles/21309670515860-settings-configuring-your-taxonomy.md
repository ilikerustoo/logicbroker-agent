---
title: "Settings: Configuring Your Taxonomy"
url: "https://support.logicbroker.com/kb/logicbroker/21309670515860-settings-configuring-your-taxonomy"
category: "Platform"
---

March 10, 2026

# Settings: Configuring Your Taxonomy

## 

**Audience :** Retailer customers 

In this article, you will find information related to Settings options available within the Product Onboarding Center. The sections within this article are outlined below:

  * Overview
  * Categories
  * Attributes
  * Attribute Sets
  * Import/Export
  * Related Content



##### Overview

The settings page provides retailers with the ability to configure their product taxonomy, to provide suppliers with the guardrails needed to drive compliance. Retailers can create their taxonomy manually in the portal, import from existing systems, or through the API. 

##### Categories 

Categories are used to organize products with similar characteristics and uses. Categories may have children and siblings (also known as levels) with different attribute sets to help create a hierarchical structure that is more defined.

**At a Glance**

**Path **– The path shows the relationship of the different categories and subcategories. This is similar to how you would see breadcrumbs at the top of a webpage. The path is structured in the following way: Category> Child > Grandchild. An example is also shown in the image below. Home and Garden >Decor > Mirrors 

**AttributeSet** – The attribute set determines the requirements for each category, sibling category, or child category that are showcased to suppliers during the product upload process. 

**Level** – The level is used in the hierarchical structure to define the positioning of a category and subcategories. i.e. the Home and Garden Category is at level 0 because it is the root category, there are 2 associated children. The first child is Decor which is at level 1 and the child of Decor is Mirrors which is at level 2. 

**Children** – This is used in the hierarchical structure to indicate the number of children or subcategories belonging to the root category. For example, the child in the example above is decor. 

**Sibling Category** – A category that belongs to the same root category but is different from other categories within that root category. For example, if the root category is clothing, some sibling categories may be tops, bottoms, and outerwear.

**Children Category** – A subcategory that falls under a parent or root category. The child is a more specific group of products that relate to the parent category. For example, if the root category is clothing, the sibling category is tops and the child category may be t-shirts or sweaters. 

##### Attributes 

Attributes allow retailers to define the different fields they would like to collect from suppliers to help describe a product.

**At a Glance**

**Name **– The name used to identify the attribute with the CSV files or API. There should be no spaces, content can be alphanumeric, lowercase, and contain underscores. i.e. parent_sku

**FriendlyName** – This is how the attribute name appears in the portal. The FriendlyName may contain spaces, capitals, etc. i.e. Parent SKU

**Type** – This provides the users with different field type options.

  * Text: Any string value used when there are differet input types. Example: Product Name - Logicbroker Tee Shirt 
  * Select: Values are provided in a dropdown field and is used when there are rules around the field. Example: Category - Appliances 
  * Number: A decimal number. This attribute is used when the answer is a numerical value. Example: Cost of Product - 42.00
  * Image: Image is downloaded into our content delivery network. 
  * Yes/no: This is a boolean value, where the field can only be one of two values. Example: Is bundle? Yes 
  * List: A collection data type that allows multiple values to be stored in a single field. 



**Description** – This provides insight into a specific attribute to better understand what is required. i.e. for the parent_sku attribute, the description may be "Unique product identifier of parent item (main variant SKU, etc.)." 

**Group** – This is used for detail grouping on the product details screen. i.e. parent_sku may be classified as a basic attribute. 

**System** – This is a boolean field that is used to indicate whether an attribute is defined by Logicbroker or not. If system is equal to true, the attribute cannot be deleted or changed. i.e. the SKU attribute 

##### Attribute Sets 

Attribute sets are groups of attributes used to create templates for information collected from the supplier. Attribute sets are also used to organize the way the data is displayed on the product detail page.

**At a Glance**

**Name **– The name used to identify the attribute set with the CSV files or API. There should be no spaces, content can be alphanumeric, lowercase, and contain underscores. i.e. attribute_set_name

**FriendlyName** – This is how the attribute set name appears in the portal. The FriendlyName may contain spaces, capitals, etc. i.e. Attribute Set Name

**System** – This is a boolean field that is used to indicate whether an attribute is defined by Logicbroker or not. If system is equal to true, the attribute cannot be deleted or changed. i.e. the base attribute set 

**DestinationId** – This is used to define the key reference in the external system where the attribute set is being synced. This may be required when pushing in data to indicate where to find this in the target system.

**Tags** – Tags are used for grouping meta-information to be attached to attributes for the purposes of umbrella classifications and other helpful associations. i.e. Tagging several attribute sets with "apparel" to make them easier to find or filter.

**Last Modified** – The date and time of the last update made to the attribute set. 

##### Import/Export 

The import and export functionality provides retailers with an easy way to bring their existing taxonomy into the portal or extract the information out of Logicbroker to use in their other systems. Logicbroker offers the ability for retailers to import their categories, attributes, and attribute sets. The export functionality can be used to export categories, attributes, attribute sets, partner products (partner catalog), and products (my catalog). 

**At a Glance**

**Profile** – The profile functionality provides the ability to save the configurations users have made for their import or export so that the next time the import or export is used, all of their preferences are readily available. Profiles can also be shared with other members within your organization. 

**Delimiter** – The delimiter is used to separate different pieces of data within the file. The supported options are comma (,), semicolon (;), pipe (|), or tab (\t). This is available on the export only. 

**Export Format** – The export format is a way for users to specify how they would like to consume the data once it leaves Logicbroker. The supported formats are CSV or XLSX. This is available on the export only. 

**Filters** – Filters provide users with the ability to tailor their export files based on specific criteria. For example, if a user only wants to export products that contain a certain word in the product name, Logicbroker will return only the items that meet the specified criteria rather than the entire catalog. This is available on export only. 

**Rules** – Rules provide the ability for users to alter data so that the data appears in the spreadsheet the way the user wants to consume it. For example, if a company was operating internationally a field such as color could have a rule applied so that the color is translated and then exported in the translated language. This is available on the export only. 

**Fields to Export** – Fields to export provides users with the ability to select the fields being extracted from Logicbroker. The input field/expression column is where users can determine what information is being exported and the output column is where the user can determine how the information appears on the exported file. For example, the input field/expression may be Name and the user may want the output column to be Product Name. This is available on the export only. 

**Column Mapping** – Column mapping provides users with the ability to take columns in their spreadsheet and match them to the field in Logicbroker. There is also the ability to add rules or conditions on applicable lines. This is available on the import only.