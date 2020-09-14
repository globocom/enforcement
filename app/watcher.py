from injector import inject
from dataclasses import dataclass

from data import RancherRepository, ArgoRepository, RancherClusterConverter
from helper import Config


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

        self._argo_repository.create_application(
            name=self._config.enforcement_name,
            cluster_name=rancher_cluster['name'],
            repo=self._config.enforcement_core_repo,
            path=self._config.enforcement_core_path
        )


