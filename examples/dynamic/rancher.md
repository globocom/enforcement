## Rancher 

All fields of cluster objects returned via the Rancher API /v3/clusters/[clusterID] are available to be used in dynamic 
configurations on ClusterRule objects. They can be accessed as Python dictionaries within the Jinja expression as the 
examples below follow.

````yaml
name: ${{name}} #cluster name
driverName: ${{genericConfig['driverName']}}
region: ${{genericConfig['region']}}
displayName: ${{appliedSpec['displayName']}}
rancherAgent: ${{agentImage}}
```

See Rancher API /v3/clusters/[clusterID] for all available fields.

