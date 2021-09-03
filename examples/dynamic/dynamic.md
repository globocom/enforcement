# Dynamic Fields 

You can use Jinja expressions to create dynamic ClusterRules.

The **name**, **url** and **id** fields are available in ClusterRules that use any Cluster sources

```yaml
name: ${{name}} #cluster name
url: ${{url}}
id: ${{id}}
```

## Dynamic Fields in Rancher Cluster Source 

All fields of cluster objects returned via the Rancher API ***/v3/clusters/[clusterID]*** are available to be used in dynamic 
configurations on ClusterRule objects. They can be accessed as Python dictionaries within the Jinja expression as the 
examples below follow.

```yaml
driverName: ${{genericConfig['driverName']}}
region: ${{genericConfig['region']}}
displayName: ${{appliedSpec['displayName']}}
rancherAgent: ${{agentImage}}
creator: ${{creatorId}}
kubernetesVersion: ${{amazonElasticContainerServiceConfig['kubernetesVersion']}}
```

See Rancher API ***/v3/clusters/[clusterID]*** for all available fields.

