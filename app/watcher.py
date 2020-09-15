from injector import inject
from dataclasses import dataclass

from model import ClusterMonitor


@inject
@dataclass
class EnforcementWatcher:
    _cluster_monitor: ClusterMonitor

    def run(self):

        for cluster in self._cluster_monitor.detect_new_clusters():
            self._cluster_monitor.register(cluster)
            cluster.enforcements.apply()

        for cluster in self._cluster_monitor.detect_deleted_clusters():
            cluster.enforcements.remove()
            self._cluster_monitor.unregister(cluster)





