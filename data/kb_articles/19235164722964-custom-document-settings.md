---
title: "Custom Document Settings"
url: "https://support.logicbroker.com/kb/logicbroker/19235164722964-custom-document-settings"
category: "Document Standards"
---

March 3, 2026

# Custom Document Settings

## 

**Audience :** EDI users

####  __ Note:

Custom document settings are not commonly used for most EDI connections. These are meant to allow users to support complex requirements. Document settings are defaulted using our standard set.

See the available customizations below. 

**Partner and Document Type**  
This will allow you to select one of your connected partners or supported document types from the dropdown to define customizations to be applied under those conditions. 

**Type Code**  
This is the 3 digit numeric value that identifies the document type that is being transmitted. This value is present in the ST segment. 

**ISA Segment**

ISA (Interchange Control Header) identifiers are used to determine the sender and receiver of the transaction. The ISA segment is found in the beginning of the document and is the outermost envelope containing the sender, receiver, date, time and control number. 

  
  


  * **Your/Partner ISA Qualifier** \- This is the two-digit code used to describe the ID. Commonly used qualifiers include: ZZ (Mutually Defined), 01 (Duns) and 12 (Phone) 
  * **Your/Partner ISA ID** \- This is the unique identifier of the sender or receiver of the data
  * **Repeat Character** \- This separates repeating occurrence of data elements or sub-elements in the same position within the same data segment context (Default: U)
  * **Element Separator** \- This separates data elements (Default: *)
  * **Request 997** \- This is the acknowledgment request indicator used to report the status of processing a received transaction or the non-delivery of a transaction (Default: 0)
  * **Sub-Element Separator** \- This is used to mark the beginning of a sub-element (Default: >)
  * **Segment Terminator** \- This determines the end of the segment (Default: ~)



**GS Segment**

The GS (Group ID) segment is the beginning of a functional group and is used to identify the application type for the interchange for the sender/receiver. 

  
  


  * **Type** \- This value defines the transaction type
  * **Your/Partner GS ID** \- This is the unique identifier of the sender or receiver of the data and is usually the same as the sender/receiver ISA ID
  * **Version** \- This identifies the version of the transaction set