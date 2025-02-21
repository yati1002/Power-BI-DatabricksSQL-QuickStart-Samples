# Power BI Service Connections to Databricks with Private Networking

## Private Networking Options for Databricks
When deploying Databricks with enhanced security, customers can choose from three main private networking configurations:
1. Public Endpoint with an [IP Access List](https://learn.microsoft.com/en-us/azure/databricks/security/network/front-end/ip-access-list) for the [Workspace](https://learn.microsoft.com/en-us/azure/databricks/security/network/front-end/ip-access-list-workspace): This option exposes a public endpoint for the Databricks workspace but restricts access to specific IP ranges.
2. [Databricks Private Link](https://learn.microsoft.com/en-us/azure/databricks/security/network/classic/private-link): Front-end private link provides fully private connectivity, routing all traffic through private endpoints.
3. Hybrid Deployment: Combines front-end private link with a public endpoint protected by a Workspace IP Access List which is typically used for SaaS service connections.

## Connecting Power BI to a Private Databricks Workspaces
While private networking enhances security, it can require additional connection configurations from SaaS services like Power BI. Power BI offers two primary methods for secure connections to data sources with private networking:
1. [On-premises data gateway](https://learn.microsoft.com/en-us/data-integration/gateway/service-gateway-onprem): an application that gets installed on a Virtual Machine that has a direct networking connection to the data source. It allows Power BI to connect to data sources that don’t allow public connections
2. [Virtual Network Data Gateway](https://learn.microsoft.com/en-us/data-integration/vnet/overview): a managed (virtual/serverless) data gateway that gets created and managed by the Power BI service.  Connections work by allowing Power BI to delegate into a VNet for secure connectivity to the data source.
While Power BI offers these two options, many customers prefer not to manage additional infrastructure or configurations required for these gateways. In such cases, Power BI can be allowed to access the private Databricks workspace through the IP Access List.

## Implementing Power BI Connectivity via IP Access List
To enable the Power BI Service connectivity to a private Databricks workspace using an IP Access List:
Obtain the Power BI Public IPs:
1. Download the latest [Azure IP Ranges and Service Tags](https://www.microsoft.com/en-us/download/details.aspx?id=56519) file from the Microsoft Download Center. This file is updated weekly and contains IP ranges for various Azure services, including Power BI.
2. Add Power BI IPs to Databricks Workspace IP Access List:
Extract the Power BI IP ranges from the downloaded file and add them to the Databricks IP Access List using the [API](https://docs.databricks.com/api/workspace/ipaccesslists) or [SDK](https://databricks-sdk-py.readthedocs.io/en/latest/workspace/settings/ip_access_lists.html). 
3. Regular Updates:
Since Power BI public IPs can change frequently, it's crucial to update the Workspace IP Access List regularly. This can be automated using a Databricks Job that periodically downloads the latest IP ranges and updates the Workspace IP Access List. The Job will need to be run by a Workspace Admin in order to set the configurations. You can run the Databricks Job as a Service Principal to make the updates. If you use the Databricks SDK from within a notebook in the Databricks Workspace, [authentication](https://databricks-sdk-py.readthedocs.io/en/latest/authentication.html#notebook-native-authentication) is handled for you.

The following sample code can be used to [turn on your Workspace IP Access List](https://github.com/yati1002/Power-BI-DatabricksSQL-QuickStart-Samples/blob/main/09.%20Private%20Connections/Turn%20on%20Workspace%20IP%20Access%20List.py) which is more of a one-time operation. The [Power BI IPs for IP Access List](https://github.com/yati1002/Power-BI-DatabricksSQL-QuickStart-Samples/blob/main/09.%20Private%20Connections/Power%20BI%20IPs%20for%20IP%20Access%20List.py) sample code can be used to refresh your Power BI IPs from a Databricks Workflow.  


