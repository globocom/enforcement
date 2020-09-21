import os
import configparser
from injector import inject


class Config:
    @inject
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        self._config = config

    @property
    def rancher_url(self):
        return os.environ.get('RANCHER_URL', None) or self._config.get('rancher', 'url')

    @property
    def rancher_token(self):
        return os.environ.get('RANCHER_TOKEN', None) or self._config.get('rancher', 'token')

    @property
    def argo_url(self):
        return os.environ.get('ARGO_URL', None) or self._config.get('argo', 'url')

    @property
    def argo_username(self):
        return os.environ.get('ARGO_USERNAME', None) or self._config.get('argo', 'username')

    @property
    def argo_password(self):
        return os.environ.get('ARGO_PASSWORD', None) or self._config.get('argo', 'password')

    @property
    def enforcement_core_repo(self):
        return os.environ.get('ENFORCEMENT_CORE_REPO', None) or self._config.get('enforcement-core', 'repo')

    @property
    def enforcement_core_path(self):
        return os.environ.get('ENFORCEMENT_CORE_PATH', None) or self._config.get('enforcement-core', 'path')

    @property
    def enforcement_name(self):
        return os.environ.get('ENFORCEMENT_NAME', None) or self._config.get('enforcement-core', 'name')