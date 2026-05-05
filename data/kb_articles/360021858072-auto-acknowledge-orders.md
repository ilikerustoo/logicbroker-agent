---
title: "Auto-Acknowledge Orders"
url: "https://support.logicbroker.com/kb/logicbroker/360021858072-auto-acknowledge-orders"
category: "Platform"
---

March 3, 2026

# Auto-Acknowledge Orders

## 

**Automatic Acknowledgements for Orders**

Sending automatic acknowledgments is a function of *Logicbroker workflows*. When an order is received by a supplier, the supplier can either systematically or manually acknowledge the order. By acknowledging the order, the supplier lets the retailer know which items they plan on fulfilling (accepting, or cancelling line items). If the supplier desires, they can use Logicbroker to send automatic acknowledgments on their behalf. This will send the necessary acknowledgment document (typically EDI 855) back to the retailer, accepting all lines and quantities.

**Example of Use**

You are a supplier connected to an EDI retailer. The retailer requires you to send 855 purchase order acknowledgments, but your system is unable to generate this data. You have the Auto-Acknowledge orders feature activated for your account (it can be activated for your entire account, or per partnership).

_Logicbroker will configure the workflow to send acknowledgements automatically_

**Setup Process**

  1. Identify if you are able to send Acknowledgments for your retailers
  2. If not, have Logicbroker setup this workflow process to auto-acknowledge your orders.