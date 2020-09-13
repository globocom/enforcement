from injector import inject
from dataclasses import dataclass

from data import RancherRepository, ArgoRepository, RancherClusterConverter
from helper import Config
from argocd_client import V1alpha1Application, V1alpha1ApplicationSpec, \
    V1alpha1ApplicationDestination, V1alpha1ApplicationSource, V1ObjectMeta, \
    V1alpha1SyncPolicy, V1alpha1SyncPolicyAutomated, V1alpha1ApplicationSourceHelm, \
    V1alpha1HelmParameter


@inject
@dataclass
class EnforcementWatcher:
    _rancher_repository: RancherRepository
    _argo_repository: ArgoRepository
    _rancher_converter: RancherClusterConverter
    _config: Config

    def run(self):
        argo_clusters_names = self._argo_repository.list_cluster_names()
        rancher_clusters = self._rancher_repository.get_clusters()

        unregistered_clusters = list(
            filter(
                lambda cluster: cluster['name'] not in argo_clusters_names,
                rancher_clusters
            )
        )

        for unregistered_cluster in unregistered_clusters:
            self._register_cluster(unregistered_cluster)

    def _register_cluster(self, rancher_cluster: dict):
        self._argo_repository.register_cluster(
            self._rancher_converter.to_argo_cluster(
                rancher_url=self._config.rancher_url,
                rancher_token=self._config.rancher_token,
                rancher_cluster=rancher_cluster,
            )
        )

        application = V1alpha1Application(
            metadata=V1ObjectMeta(
               name='guestbook-enforcement'
            ),
            spec=V1alpha1ApplicationSpec(
                destination=V1alpha1ApplicationDestination(
                    server='https://kubernetes.default.svc',
                    namespace='argocd',
                ),
                source=V1alpha1ApplicationSource(
                    path=self._config.enforcement_core_path,
                    repo_url=self._config.enforcement_core_repo,
                    helm=V1alpha1ApplicationSourceHelm(
                        parameters=[
                            V1alpha1HelmParameter(name="spec.destination.name", value=rancher_cluster['name']),
                            V1alpha1HelmParameter(name="spec.source.repoURL", value=self._config.enforcement_core_repo)
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

        self._argo_repository.register_application(application)


