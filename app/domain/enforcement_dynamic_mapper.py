from app.domain.entities import Cluster, Enforcement

from jinja2 import Template
import yaml
import requests


class EnforcementDynamicMapper:
    def __call__(self, cluster: Cluster, enforcement: Enforcement) -> Enforcement:
        yaml_enforcement = yaml.dump(enforcement.dict())
        yaml_enforcement = yaml_enforcement.replace("$", "", -1)

        t = Template(yaml_enforcement)
        cluster_dict = cluster.dict()
        cluster_dict.pop("additional_data")
        cluster_dict.update(cluster.additional_data)
        cluster_dict["requests"] = requests
        yaml_enforcement = t.render(**cluster_dict)
        enforcement_dict = yaml.load(yaml_enforcement)
        return Enforcement(**enforcement_dict)


