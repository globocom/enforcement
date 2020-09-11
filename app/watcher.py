from injector import inject
from dataclasses import dataclass
from typing import List

from service.rancher import RancherService
from helper.config import Config
from argocd_client import V1alpha1ClusterConfig, ClusterServiceApi, V1alpha1Cluster,  \
    V1alpha1ClusterList, V1alpha1TLSClientConfig, V1alpha1Application, V1alpha1ApplicationSpec, \
    V1alpha1ApplicationDestination, V1alpha1ApplicationSource, ApplicationServiceApi, V1ObjectMeta, \
    V1alpha1SyncPolicy, V1alpha1SyncPolicyAutomated


@inject
@dataclass
class EnforcementWatcher:
    _rancher_service: RancherService
    _cluster_service: ClusterServiceApi
    _application_service: ApplicationServiceApi
    _config: Config

    def run(self):
        argo_clusters_names = self._get_argo_clusters_name()
        rancher_clusters = self._rancher_service.get_clusters()

        unregistered_clusters = list(
            filter(
                lambda cluster: cluster['name'] not in argo_clusters_names,
                rancher_clusters
            )
        )

        for unregistered_cluster in unregistered_clusters:
            self._register_cluster(unregistered_cluster)

    def _register_cluster(self, rancher_cluster: dict):
        argo_cluster = V1alpha1Cluster(
            name=rancher_cluster['name'],
            server=f"{self._config.rancher_url}/k8s/clusters/{rancher_cluster['id']}",
            config=V1alpha1ClusterConfig(
                bearer_token=self._config.rancher_token,
                tls_client_config=V1alpha1TLSClientConfig(insecure=True)
            ),
        )

        self._cluster_service.create(argo_cluster)

        application = V1alpha1Application(
            metadata=V1ObjectMeta(
               name='guestbook-enforcement'
            ),
            spec=V1alpha1ApplicationSpec(
                destination=V1alpha1ApplicationDestination(
                    name=rancher_cluster['name'],
                    namespace='default',
                ),
                source=V1alpha1ApplicationSource(
                    path='guestbook',
                    repo_url='https://github.com/ribeiro-rodrigo-exemplos/argocd-example-apps.git'
                ),
                sync_policy=V1alpha1SyncPolicy(
                    automated=V1alpha1SyncPolicyAutomated(
                        prune=False,
                        self_heal=True,
                    )
                )
            )
        )

        self._application_service.create_mixin9(application)

    def _get_argo_clusters_name(self) -> List[str]:
        argo_clusters: V1alpha1ClusterList = self._cluster_service.list()
        names = [item.name for item in argo_clusters.items]
        return names

