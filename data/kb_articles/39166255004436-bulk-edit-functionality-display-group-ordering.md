---
title: "Bulk Edit Functionality & Display Group Ordering"
url: "https://support.logicbroker.com/kb/logicbroker/39166255004436-bulk-edit-functionality-display-group-ordering"
category: "Platform"
---

March 12, 2026

# Bulk Edit Functionality & Display Group Ordering

## 

### Audience

This guide applies to all retailers and suppliers using Logicbroker's Product Onboarding Center (POC) who want to utilize the new Bulk Edit functionality within the portal. It also covers an internal-only display group ordering feature available by request.

### Overview

Logicbroker's Product Onboarding Center (POC) continues to evolve to support faster, more efficient product data management for both retailers and suppliers. This guide introduces the new Bulk Edit feature, designed to streamline updates across multiple products directly within the portal UI. Whether you're updating pricing due to market changes, modifying descriptions, or applying tags across dozens of SKUs, Bulk Edit provides a user-friendly interface that eliminates the need for manual CSV exports and reimports in many cases.

In addition to the Bulk Edit tool, this guide outlines a behind-the-scenes enhancement for reordering display groups on the product detail page. Though limited in scope and intended for internal Logicbroker teams, this feature addresses display order customization for specific clients with unique data needs.

Together, these tools improve operational agility, reduce dependency on technical workflows, and make product updates more intuitive and accessible, especially for users managing moderate-scale updates.

* * *

###### Bulk Edit Functionality

### What is it?

The Bulk Edit feature allows users to update multiple product attributes simultaneously within the Logicbroker portal without requiring CSV exports and reimports. This is ideal for small to medium-sized edits across up to 100 products at a time.

### Why it Matters

Previously, bulk changes required exporting and reimporting CSV files. The new Bulk Edit tool offers a simpler, more user-friendly option directly in the UI for quick, mid-sized updates.

##### Step-by-Step Instructions

#### 1\. Selecting Products

  * Navigate to the Product Onboarding Center.
  * Apply search or filter criteria to locate the products you want to update (e.g., by tag, supplier, catalog, etc.).
  * Adjust the page size to display up to 100 products at a time.
  * Select the products you wish to edit using the checkboxes.



#### 2\. Launching Bulk Edit

  * Click the **Edit** button in the Bulk Actions toolbar.




#### 3\. Choosing Attributes to Edit

  * In the Bulk Edit wizard, select the attributes you wish to update (e.g., price, tags, description).




#### 4\. Setting Update Operations

  * **For Numeric Fields (e.g., Price)**
    * Options: Increase by %, Decrease by %, Set to fixed value
  * **For Text Fields (e.g., Description)**
    * Options: Replace, Add to existing, Clear field
  * **For Tags**

    * Options: Add to existing, Remove specific tags, Replace all, Clear all tags (Note: system tags like Logicbroker tags are protected and cannot be removed)



#### 5\. Review Changes

  * The wizard will show current and updated values for each selected product.
  * A backup CSV will automatically generate in case rollback is needed.




#### 6\. Execute Bulk Edit

  * Confirm and execute the changes.
  * Optionally download the backup CSV.
  * Backup CSVs can also be accessed in **Files - > Attachments** tab found within the left navigation panel




### Important Notes

  * Bulk Edit is limited to **100 products per session.** For large updates, use the CSV export/import method.
  * Tags critical to system functionality (e.g., Logicbroker connector tags) **cannot be removed** , even if "Clear all tags" is selected.
  * Price changes in POC **do not impact inventory prices.** Inventory prices must be updated separately.
  * Bulk Edit applies updates across **multiple products/variants**. Single product updates can still be made in the Product Details view.



### Bulk Edit vs. Variant Edits

Feature | Bulk Edit | Product Detail Edits  
---|---|---  
Scope | Multiple products (up to 100) | Single product  
Purpose | Large scale changes | Fine-tuning individual products  
Typical Use Case | Price increases, tag updates | Detailed variant adjustments  
Applies To | Variants across products | Variants within one product  
  
### Frequently Asked Questions

#### Q: Can I bulk edit more than 100 products at once?

**A:** No. Bulk Edit is limited to 100 products per session due to system constraints. For larger updates, use the CSV export/import method.

#### Q: Can I remove all tags from products?

**A:** System-critical tags, like Logicbroker connector tags, are protected and cannot be removed even if "Clear all tags" is selected.

#### Q: Do price updates in POC affect inventory pricing?

**A:** No. Inventory prices must be managed separately. POC price changes will not sync to inventory systems.

#### Q: What’s the difference between Bulk Edit and variant-level edits?

**A:** Bulk Edit applies changes across multiple products. Variant-level edits occur within a single product view.

* * *

###### Display Group Ordering (Internal-Only Feature)

### What is it?

A limited feature that allows internal Logicbroker teams to reorder display groups on the product details page for select retailers.

### How it Works

  * Available via attribute file export and manual prefix adjustments.
  * **Basics** and **Media** groups are fixed in positions 1 and 2 and cannot be moved.




### Steps:

  1. Export attribute file from Taxonomy settings.
  2. Add numeric prefixes (e.g., "3. Product Warnings") to the Group Name field.
  3. Reimport the file.
  4. The system will sort display groups based on the numeric prefix.



> **Note:** This is a one-time setup handled by Logicbroker support teams. It is not a client-facing feature and is not accessible via drag-and-drop in the UI.

### Key Reminders

  * The prefix is stripped from the display name in the portal.
  * This feature is not widely advertised or generally available.
  * Future UI updates may include drag-and-drop support.