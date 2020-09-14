from dataclasses import dataclass
from injector import inject
from typing import List

from argocd_client import ClusterServiceApi, V1alpha1Cluster, V1alpha1ApplicationDestination,  \
    V1alpha1ClusterList, V1alpha1Application, V1alpha1ApplicationSpec, V1alpha1ApplicationSource, \
    ApplicationServiceApi, V1ObjectMeta, V1alpha1SyncPolicy, V1alpha1SyncPolicyAutomated, \
    V1alpha1ApplicationSourceHelm, V1alpha1HelmParameter


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

    def create_application(self, name, cluster_name, repo, path):

        application = V1alpha1Application(
            metadata=V1ObjectMeta(
               name=name
            ),
            spec=V1alpha1ApplicationSpec(
                destination=V1alpha1ApplicationDestination(
                    name='in-cluster',
                    namespace='argocd',
                ),
                source=V1alpha1ApplicationSource(
                    path=path,
                    repo_url=repo,
                    helm=V1alpha1ApplicationSourceHelm(
                        parameters=[
                            V1alpha1HelmParameter(name="spec.destination.name", value=cluster_name),
                            V1alpha1HelmParameter(name="spec.source.repoURL", value=repo)
                        ]
                    )
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

