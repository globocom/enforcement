from injector import inject

from argocd_client import V1alpha1Cluster, V1alpha1ClusterConfig, V1alpha1TLSClientConfig


class RancherClusterConverter:
    @inject
    def __init__(self):
        pass

    def to_argo_cluster(self, rancher_cluster, rancher_url, rancher_token) -> V1alpha1Cluster:
        argo_cluster = V1alpha1Cluster(
            name=rancher_cluster['name'],
            server=f"{rancher_url}/k8s/clusters/{rancher_cluster['id']}",
            config=V1alpha1ClusterConfig(
                bearer_token=rancher_token,
                tls_client_config=V1alpha1TLSClientConfig(insecure=True)
            ),
        )
        return argo_cluster
