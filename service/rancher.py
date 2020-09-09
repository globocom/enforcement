from helper.config import Config


class RancherService:
    def __init__(self, config: Config):
        self._config = config

    def get_clusters(self) -> str:
        return self._config.rancher_url

