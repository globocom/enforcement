from app.data.source.definition.register import SourceRegister
from app.domain.entities import EnforcementSource
from app.domain.repositories import SourceRepository
from app.domain.source_locator import SourceLocator
from app.infra.config import Config
from app.infra.kubernetes_helper import KubernetesHelper


class SourceLocatorImpl(SourceLocator):

    def __init__(self, config_helper: Config, kubernetes_helper: KubernetesHelper):
        self._config_helper = config_helper
        self._kubernetes_helper = kubernetes_helper
        self._secret = None

    def locate(self, source: EnforcementSource) -> SourceRepository:
        source_name = list(source.__dict__.keys())[0]
        datasource_class = SourceRegister.find_source(source_name)
        secret_name = source.secretName if source.secretName is not None else source_name

        self._secret = self._kubernetes_helper.get_secret(secret_name)

        if not datasource_class:
            raise Exception("Source not defined")

        return datasource_class(config=self._config_helper, source=source, kubernetes_helper=self._kubernetes_helper,
                                secret=self._secret)
