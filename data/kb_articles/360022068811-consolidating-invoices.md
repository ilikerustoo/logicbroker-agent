---
title: "Consolidating Invoices"
url: "https://support.logicbroker.com/kb/logicbroker/360022068811-consolidating-invoices"
category: "Platform"
---

March 3, 2026

# Consolidating Invoices

## 

There are going to be instances where a retailer does not want to receive an invoice for every shipment that is sent out, but rather they would like to receive an invoice per Purchase Order Number. Logicbroker has the ability using *_ **Logicbroker Workflows**_ * to receive multiple shipments per PO and then send over one invoice per that same PO Number. The breakdown of the invoice will show all line items that were fulfilled, rather than sending one invoice per PO, per line. This is beneficial for those retailers who may not accept multiple invoices per PO Number.

This is particularly helpful for big replenishment orders where shipments may have to be split out because of the size.

**Setup Process**

  1. When working with the Retailer, Logicbroker will determine if this consolidation is required.
  2. Logicbroker will configure the workflows and address information accordingly.
  3. Test the mappings and ensure that everything is flowing into your system and back to the retailer as expected.