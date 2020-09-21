from injector import inject
from dataclasses import dataclass

from model.cluster_monitor import ClusterMonitor


@inject
@dataclass
class EnforcementWatcher:
    _cluster_monitor: ClusterMonitor

    def run(self):

        for cluster in self._cluster_monitor.detect_new_clusters():
            self._cluster_monitor.register(cluster)
            cluster.apply_all_enforcements()

        for cluster in self._cluster_monitor.detect_deleted_clusters():
            cluster.remove_all_enforcements()
            self._cluster_monitor.unregister(cluster)





