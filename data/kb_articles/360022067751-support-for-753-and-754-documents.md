---
title: "Support for 753 and 754 Documents"
url: "https://support.logicbroker.com/kb/logicbroker/360022067751-support-for-753-and-754-documents"
category: "Document Standards"
---

March 10, 2026

# Support for 753 and 754 Documents

## 

[🔗Amazon Vendor Central (Routing).docx](https://support.logicbroker.com/hubfs/logicbroker_media/Amazon%20Vendor%20Central%20\(Routing\).docx?hsLang=en) (700 KB)  
---  
  
Routing requests (753) and routing instructions (754) are used by retailers to add better visibility and control to their supply chain. As a supplier or brand, some retailers will require using this document flow.[](https://support.logicbroker.com/hubfs/Knowledge%20Base%20Import/Support%20for%20753%20and%20754%20Documents_Workflow-3.png?hsLang=en)

In general, a routing request is initiated and sent by the supplier to let the retailer know they are ready for a shipment to be scheduled. The routing request contains all the standard information you would find on a shipment (ASN) document.

In Logicbroker, when a shipment is created, the 753 will send automatically and move your shipment document to the "**Awaiting 754** " status. At this stage, the shipment will wait for the 754 Routing Instructions to be received from the retailer.

[](https://support.logicbroker.com/hubfs/Knowledge%20Base%20Import/Support%20for%20753%20and%20754%20Documents_ShipmentDetails-3.png?hsLang=en)

The 754 Routing Instructions will contain details such as pickup date, carrier information, reference numbers and other information required on the ASN (856). The status of the shipment will move to "**754 Received** " and will wait until the order is picked up by the carrier.

[](https://content.screencast.com/users/Logicbroker/folders/KB%20Screenshots/media/7fa45df9-b549-4dbe-b8d6-008dc798f4d7/Support%20for%20753%20and%20754%20Documents_ShipmentDetailsEventDetails.PNG)

Lastly, once your shipment is picked up by a carrier, you can now submit the Shipment (ASN/856) document indicating that it has been physically shipped. You can do this by clicking "**COMPLETE SHIPMENT** " next to More Actions. 

This will send the ASN, move the shipment to a complete status and in turn update the Order to indicate it has shipped as well.

[](https://support.logicbroker.com/hubfs/Knowledge%20Base%20Import/Support%20for%20753%20and%20754%20Documents_ShipmentDetailsComplete-3.png?hsLang=en)