import os
import configparser
from injector import inject
from typing import List


class Config:
    @inject
    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read("config.ini")
        self._config = config

    @property
    def rancher_url(self) -> str:
        return os.getenv('RANCHER_URL') or self._config.get('rancher', 'url')

    @property
    def rancher_token(self) -> str:
        return os.getenv('RANCHER_TOKEN') or self._config.get('rancher', 'token')

    @property
    def argo_url(self) -> str:
        return os.getenv('ARGO_URL') or self._config.get('argo', 'url')

    @property
    def argo_username(self) -> str:
        return os.getenv('ARGO_USERNAME') or self._config.get('argo', 'username')

    @property
    def argo_password(self) -> str:
        return os.getenv('ARGO_PASSWORD') or self._config.get('argo', 'password')

    @property
    def enforcement_core_repo(self) -> str:
        return os.getenv('ENFORCEMENT_CORE_REPO') or self._config.get('enforcement-core', 'repo')

    @property
    def enforcement_core_path(self) -> str:
        return os.getenv('ENFORCEMENT_CORE_PATH') or self._config.get('enforcement-core', 'path')

    @property
    def enforcement_name(self) -> str:
        return os.getenv('ENFORCEMENT_NAME') or self._config.get('enforcement-core', 'name')

    @property
    def ignore_clusters(self) -> List[str]:

        try:
            clusters_str: str = os.getenv('IGNORE_CLUSTERS') or self._config.get('rancher', 'ignore_clusters')
            clusters = list(map(lambda cluster: cluster.strip(), clusters_str.split(",")))
            return clusters
        except configparser.NoOptionError:
            return []
