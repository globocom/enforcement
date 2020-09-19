from dataclasses import dataclass
from injector import inject

from model import Enforcement

from argocd_client import V1alpha1ApplicationDestination, V1alpha1Application, V1alpha1ApplicationSpec, \
    ApplicationServiceApi, V1ObjectMeta, V1alpha1SyncPolicy, V1alpha1SyncPolicyAutomated


@inject
@dataclass
class EnforcementRepository:
    _application_service: ApplicationServiceApi

    def create_enforcement(self, cluster_name: str, enforcement: Enforcement):

        application = V1alpha1Application(
            metadata=V1ObjectMeta(
               name=f"{cluster_name}-{enforcement.name}"
            ),
            spec=V1alpha1ApplicationSpec(
                destination=V1alpha1ApplicationDestination(
                    name=cluster_name
                ),
                source=enforcement.render(),
                sync_policy=V1alpha1SyncPolicy(
                    automated=V1alpha1SyncPolicyAutomated(
                        prune=False,
                        self_heal=True,
                    )
                )
            )
        )

        self._application_service.create_mixin9(application)

