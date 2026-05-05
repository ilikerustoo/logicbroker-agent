---
title: "Environments: Stage vs. Production"
url: "https://support.logicbroker.com/kb/logicbroker/360022058031-environments-stage-vs-production"
category: "Retailer Onboarding"
---

March 3, 2026

# Environments: Stage vs. Production

## 

For every account in the Logicbroker platform, a stage environment will be configured to help test all integrations. In the stage environment, all API URLs, FTP/SFTP locations, and systems will be configured with the stage host. 

Link to Stage: <https://stageportal.logicbroker.com/>

Link to Production: <https://portal.logicbroker.com/>

All user login and password info will be the same across the two environments. 

**Connection Differences: Stage vs. Production**

There will be some differences for connecting to stage listed below.

**FTP/SFTP**

As mentioned previously all user login information and directories will remain the same across the environments however the hosts will change; see below.

**Production:** vftp.logicbroker.com

**Stage:** vftp-stage.logicbroker.com

**API**

When testing your API integration, all API URLs, API keys will be different between the 2 environments. If you are using OAuth to connect, your username and password will be the same.

**Production API Reference:**[commerceapi.io](http://help.logicbroker.com/hc/en-us/articles/commerceapi.io?hsLang=en)

**Stage API Reference:**[stage.commerceapi.io](http://help.logicbroker.com/hc/en-us/articles/stage.commerceapi.io?hsLang=en)

**System**

If you are integrating a system, such as SAP or Magento, it is best practice to provision a sandbox to connect to the Logicbroker staging environment. If you do not have one, we can connect our stage portal to your production system to provision tests and move the configuration to production when testing is complete.