---
title: "Auto-Invoice From Shipment"
url: "https://support.logicbroker.com/kb/logicbroker/360022068931-auto-invoice-from-shipment"
category: "Platform"
---

March 3, 2026

# Auto-Invoice From Shipment

## 

**Automatic Invoices from Shipments**

Automatic invoicing is a Logicbroker configuration for a company. It can be configured for all partners, or specific to partners that request electronic invoices. When enabled, Logicbroker will use the data received on the shipment, to create an invoice to send to your trading partner. This includes all line item information (cost, price, quantity, etc.). The invoice will be created in Logicbroker’s standard format, but will be exported in the format of the receiving party. This enables the invoice to be mapped more easily to different trading partner’s specifications.

**Example of Use**

You are a supplier connected to an EDI retailer. The retailer requires you to send 810 EDI (invoices), but your system does not generate these by default. Your system does however generate shipments. You can have the auto-invoice feature enabled, so that Logicbroker will generate your invoices based off of the shipment data received.

_Auto invoicing is a feature that is configured by your onboarding representative  
  
_

__

_Invoices can also be setup on a per-partner basis_

__

**Setup Process**

  1. Identify if you need to send invoices to your trading partners
  2. If invoices are required, but you are unable to transmit them, contact your onboarding representative
  3. Your onboarding representative will configure/activate this feature for you