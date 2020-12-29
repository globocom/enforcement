from kubernetes import client, config
import base64

def get_secret(secret_name: str) -> client.V1Secret:
    api = get_kubernetes_api()
    return api.read_namespaced_secret('rancher-secret', 'default')

def get_kubernetes_api() -> client.CoreV1Api:
    config.load_kube_config()
    api = client.CoreV1Api()
    return api

def decode_secret(secret: client.V1Secret) -> dict:
    return  {k: base64.b64decode(v).decode() for k, v in secret._data.items()}