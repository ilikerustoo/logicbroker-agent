---
title: "Create Cancellations from Shipments"
url: "https://support.logicbroker.com/kb/logicbroker/360022068831-create-cancellations-from-shipments"
category: "Platform"
---

March 3, 2026

# Create Cancellations from Shipments

## 

**Create Cancellations from Shipments**

Creating cancellations from shipments is a function of partnership configurations. Within Logicbroker, the acknowledgment document allows cancellations to be communicated to retailers. This configuration assists retailers or suppliers who do not have the ability to send an acknowledgment document. When enabled, the configuration will look at the QuantityCancelled value on the shipment, and then convert the shipment format into an acknowledgment document. That acknowledgment will then be sent with the cancellation quantity and reason(s) on it. This functionality can be setup for your entire integration, or per partnership.

**Example of Use**

You are a supplier, but do not have the ability to transmit acknowledgment documents to your retailers. Since many of your retailers require EDI acknowledgments (855), and you already send shipments to Logicbroker, you will append cancellation data to the shipment you send. This data will then be mapped to the correct field by Logicbroker, so that a cancellation can be generated for the retailers requiring this data.

**Setup Process**

  1. Identify retailer requirements – retailer requires POAck, or Acknowledgment document
  2. Identify your system capabilities
  3. If unable to send acknowledgments, contact Logicbroker
  4. Have Logicbroker setup Auto-Ack, as well as Cancellation process