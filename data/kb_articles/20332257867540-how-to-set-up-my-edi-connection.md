---
title: "How to set up my EDI connection"
url: "https://support.logicbroker.com/kb/logicbroker/20332257867540-how-to-set-up-my-edi-connection"
category: "Document Standards"
---

March 3, 2026

# How to set up my EDI connection

## 

**Audience :** EDI users

####  __ Note:

Your EDI connection will only be applied to the enviornment you set them up in. Please remember to add a new EDI connection in production once you are live. 

**Step 1. Add your EDI identifiers  
** In the **My EDI Identifiers** section, click on **Add custom identifiers** and enter in your Qualifier and ID. If you want to set up unique identifiers for a partner, indicate the partner in the dropdown. Otherwise, we will default it to All partners.  
  


****Step 2.** Upload your AS2 certificate (only for AS2 users)  
**If you plan on using an AS2 connection, in the **My AS2 Certificates** section, click on **Add a new AS2 certificate**. You'll use this later when you create your connection.   
If you do not plan on using an FTP/SFTP connection, you can skip this step.  
  


****Step 3.** Add your connection details  
**Your setup will depend on the connection method you plan on using. Logicbroker-hosted SFTP will be enabled by default.  
  


  1. Continue with the default or update your connection - Click on **Edit** and select a new method from the **Connection method** dropdown. See callouts below:  

     * Logicbroker-hosted SFTP - The username will be your Logicbroker account number and your password will be your API key, which you can generate from this page. API keys can be managed from the [API Authentication](https://stageportal.logicbroker.com/profile/api-authentication) page. 

     * AS2 - Be sure to upload a certificate in the **My AS2 Certificates** section first. Once added, it will appear in the **MY AS2 Certificate** dropdown.  


  2. Show advanced options (optional) - Enter in additional details in the **Advanced options** section if needed. These differ depending on the connection type and will allow you specify a partner, document type, file mask etc.  

  3. Collect Logicbroker's connection details - For FTP/AS2 connections, you'll see the details you need from our system to create a successful conneciton on your side. This will include connection address, our AS2 certificate, etc.   

  4. Test the connection - Click on **Test connection** to confirm it is working properly. You can either use our sample data or upload a file. You will also have the ability to edit the Sender/Receiver Qualifier/ID.   

  5. Add a connection override (optional) - If you wish to have separate connections running for specific partners or document types, you can configure this by adding a connection override and specifying the partner or document type.  
  




****Step 4.** Save and Enable your connection  
**Once you have your connection details added from the **My EDI Connection** section, be sure to hit **Save**. If you are ready to have this deployed to the environment you are in, click on **Enable**. Saving will not automatically enable your new setup. This allows you to start your setup and come back to it at a later date when you wish to implement it.  
  


****Step 5.** Add a custom document setting (optional)  
**This step is optional. It is not common you will need to add a custom document setting, but if you do, you can do so from the **My Custom Document Settings** section. Either edit the default or **Add a document setting override** specific to a partner or document type. This section allows you to customize transaction data such as segment terminator, element separators, etc.  
  


****Step 6.** View your partner's EDI connection details  
**The Your Partner's Test EDI Connection Details section will provide you with your partner's Qualifier/ID and EDI specifications (if applicable). Use this data to configure the Qualifier/ID in your system and map to your partner's specifications.