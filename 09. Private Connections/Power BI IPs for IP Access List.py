# Databricks notebook source
# MAGIC %md
# MAGIC ### Obtain Updated Download Link
# MAGIC The download link at https://www.microsoft.com/en-us/download/details.aspx?id=56519 changes periodically so the `download_url` parameter below needs to be updated.

# COMMAND ----------


download_url = "https://download.microsoft.com/download/7/1/D/71D86715-5596-4529-9B13-DA13A5DE5B63/ServiceTags_Public_20250210.json"
label = "powerbi"

# COMMAND ----------

import requests
import json
import ipaddress
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import settings

# COMMAND ----------

# MAGIC %md
# MAGIC ### Download the Power BI IPs

# COMMAND ----------

# List of services we're interested in
target_services = [
"PowerBI"
]
# "PowerPlatformInfra.WestUS",
# "PowerPlatformPlex.WestUS",
# "PowerQueryOnline.WestUS",

# COMMAND ----------

def get_powerbi_ips():
    # URL of the JSON file
    url = download_url

    # Download the JSON file
    response = requests.get(url)
    data = response.json()
    
    # Filter the IP addresses
    filtered_ips = []

    for value in data["values"]:
        if any(service in value["name"] for service in target_services):
            for address_prefix in value["properties"]["addressPrefixes"]:
                # Filter out IPv6 addresses
                try:
                    ip = ipaddress.ip_network(address_prefix)
                    if ip.version == 4:
                        filtered_ips.append(address_prefix)
                except ValueError:
                    # Skip invalid IP addresses
                    pass

    # Remove duplicates and sort the list
    filtered_ips = sorted(list(set(filtered_ips)))
    return filtered_ips

# COMMAND ----------

filtered_ips = get_powerbi_ips()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Create Power BI IP Access Lists

# COMMAND ----------

def list_ip_access_lists():
    w = WorkspaceClient()
    all_lists = w.ip_access_lists.list()
    return all_lists

# COMMAND ----------

def get_filtered_list_id(list, label):
    filtered_list_id = None
    for ip_list in list:
        if ip_list.label == label:
            filtered_list_id = [True, ip_list.list_id]
            break
        else:
            filtered_list_id = [False, "0"]

    return filtered_list_id

# COMMAND ----------

def update_ip_access_list(exists, powerbi_list_id, filtered_ips):
    w = WorkspaceClient()
    if exists:
        replaced = w.ip_access_lists.replace(ip_access_list_id=powerbi_list_id,
                                             label=label,
                                             enabled=True,
                                             ip_addresses=filtered_ips,
                                             list_type=settings.ListType.ALLOW)
        print("Updated")
        return replaced
    else:
        created = w.ip_access_lists.create(label=label,
                                           ip_addresses=filtered_ips,
                                           list_type=settings.ListType.ALLOW)
        print("Created")
        return created

# COMMAND ----------

all_list = list_ip_access_lists()

# COMMAND ----------

list_id = get_filtered_list_id(all_list, label)

# COMMAND ----------

update_list = update_ip_access_list(list_id[0], list_id[1], filtered_ips)
update_list