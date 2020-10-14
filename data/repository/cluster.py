from dataclasses import dataclass
from typing import Dict, List

from argocd_client import (
    ClusterServiceApi,
    V1alpha1Cluster,
    V1alpha1ClusterList,
    V1alpha1ClusterConfig,
    V1alpha1TLSClientConfig,
)
from injector import inject

from model.entities import Cluster


@inject
@dataclass
class ClusterRepository:
    _cluster_service: ClusterServiceApi

    def list_clusters_info(self) -> List[Dict[str, str]]:
        argo_clusters: V1alpha1ClusterList = self._cluster_service.list()

        info = [
            {"name": item.name, "url": item.server}
            for item in argo_clusters.items if item.name != 'in-cluster'
        ]

        return info

    def unregister_cluster(self, cluster: Cluster) -> None:
        self._cluster_service.delete(server=cluster.url, name=cluster.name)

    def register_cluster(self, cluster: Cluster) -> None:
        argo_cluster = V1alpha1Cluster(
            name=cluster.name,
            server=cluster.url,
            config=V1alpha1ClusterConfig(
                bearer_token=cluster.token,
                tls_client_config=V1alpha1TLSClientConfig(insecure=True)
            ),
        )
        self._cluster_service.create(argo_cluster)
