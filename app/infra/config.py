import configparser
import os
from typing import List

from injector import inject


class Config:
    @inject
    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read("config.ini")
        self._config = config

    @property
    def rancher_url(self) -> str:
        return self.__get_config_value('RANCHER_URL', 'rancher', 'url')

    @property
    def rancher_token(self) -> str:
        return self.__get_config_value('RANCHER_TOKEN', 'rancher', 'token')

    @property
    def argo_url(self) -> str:
        return self.__get_config_value('ARGO_URL', 'argo', 'url')

    @property
    def argo_username(self) -> str:
        return self.__get_config_value('ARGO_USERNAME', 'argo', 'username')

    @property
    def argo_password(self) -> str:
        return self.__get_config_value('ARGO_PASSWORD', 'argo', 'password')

    @property
    def enforcement_core_repo(self) -> str:
        return self.__get_config_value('ENFORCEMENT_CORE_REPO', 'enforcement-domain', 'repo')

    @property
    def enforcement_core_path(self) -> str:
        return self.__get_config_value('ENFORCEMENT_CORE_PATH', 'enforcement-domain', 'path')

    @property
    def enforcement_name(self) -> str:
        return self.__get_config_value('ENFORCEMENT_NAME', 'enforcement-domain', 'name')

    @property
    def ignore_clusters(self) -> List[str]:
        try:
            clusters_str = self.__get_config_value(
                'IGNORE_CLUSTERS', 'rancher', 'ignore_clusters'
            )
            clusters = [cluster.strip() for cluster in clusters_str.split(',')]
            return clusters
        except configparser.NoOptionError:
            return []

    def __get_config_value(
            self, environemnt_variable_name: str, config_name: str, config_attribute: str,
    ) -> str:
        return (
            os.getenv(environemnt_variable_name)
            or self._config.get(config_name, config_attribute)
        )
