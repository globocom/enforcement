from dataclasses import dataclass
from injector import inject
from typing import List

from helper.config import Config
from argocd_client import V1alpha1ClusterConfig, ClusterServiceApi, V1alpha1Cluster,  \
    V1alpha1ClusterList, V1alpha1TLSClientConfig, V1alpha1Application, V1alpha1ApplicationSpec, \
    V1alpha1ApplicationDestination, V1alpha1ApplicationSource, ApplicationServiceApi, V1ObjectMeta, \
    V1alpha1SyncPolicy, V1alpha1SyncPolicyAutomated


@inject
@dataclass
class ArgoRepository:
    _cluster_service: ClusterServiceApi
    _application_service: ApplicationServiceApi

    def list_cluster_names(self) -> List[str]:
        argo_clusters: V1alpha1ClusterList = self._cluster_service.list()
        names = [item.name for item in argo_clusters.items]
        return names

    def register_cluster(self, cluster: V1alpha1Cluster):
        self._cluster_service.create(cluster)

    def register_application(self, application: V1alpha1Application):
        self._application_service.create_mixin9(application)
