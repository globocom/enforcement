from injector import Injector
import kopf

from di.argo_module import ArgoModule
from controller.cluster_group import ClusterGroupController

injector = Injector([
    ArgoModule()
])

if __name__ == "main":
    cluster_group_controller = injector.get(ClusterGroupController)
    decorate = kopf.on.create('enforcement.globo.com', 'v1beta1', 'clustergroups')
    decorate(cluster_group_controller.create)
