# Private Networking Options for Azure Databricks
When deploying Azure Databricks with enhanced security, customers can choose from three main private networking configurations:
1. Public Endpoint with an IP Access List for the Workspace: This option exposes a public endpoint for the Azure Databricks workspace but restricts access to specific IP ranges.
2. Azure Databricks Private Link: Front-end private link provides fully private connectivity, routing all traffic through private endpoints.
3. Hybrid Deployment: Combines front-end private link with a public endpoint protected by a Workspace IP Access List which is typically used for SaaS service connections.

# Connecting Power BI to a Private Azure Databricks Workspaces
While private networking enhances security, it can require additional connection configurations from SaaS services like Power BI. Power BI offers two primary methods for secure connections to data sources with private networking:
1. On-premises data gateway: an application that gets installed on a Virtual Machine that has a direct networking connection to the data source. It allows Power BI to connect to data sources that don’t allow public connections
2. Virtual Network Data Gateway: a managed (virtual/serverless) data gateway that gets created and managed by the Power BI service.  Connections work by allowing Power BI to delegate into a VNet for secure connectivity to the data source.
While Power BI offers these two options, many customers prefer not to manage additional infrastructure or configurations required for these gateways. In such cases, Power BI can be allowed to access the private Azure Databricks workspace through the IP Access List.

# Implementing Power BI Connectivity via IP Access List
To enable the Power BI Service connectivity to a private Azure Databricks workspace using an IP Access List:
Obtain the Power BI Public IPs:
1. Download the latest Azure IP Ranges and Service Tags file from the Microsoft Download Center. This file is updated weekly and contains IP ranges for various Azure services, including Power BI.
2. Add Power BI IPs to Azure Databricks Workspace IP Access List:
Extract the Power BI IP ranges from the downloaded file and add them to the Azure Databricks IP Access List using the API or SDK. 
3. Regular Updates:
Since Power BI public IPs can change frequently, it's crucial to update the Workspace IP Access List regularly. This can be automated using a Databricks Job that periodically downloads the latest IP ranges and updates the Workspace IP Access List. The Job will need to be run by a Workspace Admin in order to set the configurations. You can run the Databricks Job as a Service Principal to make the updates. If you use the Databricks SDK from within a notebook in the Databricks Workspace, authentication is handled for you.

