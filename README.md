# Enforcement
## Introduction
Enforcement is a service responsible for integrating clusters orchestrated by Rancher to ArgoCD, making it possible for the clusters to use the benefits of GitOps at the same time they are created.

Enforcement also allows you to configure a GIT repository with standard applications that must be installed on all clusters created by Rancher.

## How does it work?

The Enforcement service lists all the clusters orchestrated by Rancher through its API Rest. After obtaining all the clusters, the service configures all of them on the ArgoCD and requests the installation of the standard applications present in the configured Git repository. ArgoCD installs all applications on the configured clusters and guarantees that they will always be installed.

\
![alt text](https://raw.githubusercontent.com/globocom/enforcement-service/master/architecture.png)

## Installation 

Enforcement can be installed on Kubernetes using a helm chart. See the following page for information on how to get Enforcement up and running.
\
\
[Installing the helm chart](https://github.com/globocom/charts/tree/master/sources/enforcement)

## Running Local 
Install the dependencies using PipEnv. 

```shell
pipenv install 
```
activate the Pipenv shell. 

```shell
pipenv shell
```
Run the application. 
```shell
python main.py
```
It is also possible to run the application through Docker.
\
Build the Docker image. 
```shell
docker build -t enforcement . 
```
Run container. 
```shell
docker container run --env VARIABLE1=value --env VARIABLE2=value enforcement
```

## Configuration 
Enforcement uses the environment variables described in the table below. 

| Environment Variable |      Example     |          Description         |
|:--------------------:|:----------------:|:----------------------------:|
| RANCHER_URL                | https://myrancherurl.domain.com               | Rancher URL         |
| RANCHER_TOKEN              | token-q5bhr:xtcd5lbzlg6mhnvncwbrk55zvmh       | Rancher API Key configured without scope |
| IGNORE_CLUSTERS            | "cluster1, cluster2, cluster3"                | Name of clusters orchestrated by Rancher that should be ignored by Enforcement     |
| ARGO_URL                   | https://myargourl.domain.com                  | Argo URL          |
| ARGO_USERNAME              | admin                                         | Argo Username            |
| ARGO_PASSWORD              | password                                      | Argo Password
| ENFORCEMENT_CORE_REPO      | https://github.com/globocom/enforcement-core-example.git | Git repository that contains the standard packages that must be installed in all clusters created by Rancher. | 
| ENFORCEMENT_CORE_PATH      | standard                                      | Path within the Git repository configured at ENFORCEMENT_CORE_REPO that contains the standard packages| 
| ENFORCEMENT_NAME           | standard                                      | Name of the standard application created in Argo for each cluster created by Rancher|

## Enforcement Core Repository
The Enforcement Service allows you to configure a repository containing applications that must be installed in all clusters created by Rancher. This can be useful if you want to install certain packages that need to be present in all clusters.
For example, you may want to install CNI Calico or FluentD daemonset for log collection whenever a new cluster is created. 
\
\
The Enforcement Core Repository uses the ArgoCD [App Of Apps](https://argoproj.github.io/argo-cd/operator-manual/cluster-bootstrapping/) standard for configuring standard applications.
The standard repository should be structured as follows:

```
.
├── standard
|   ├── Chart.yaml
|   └── values.yaml
|   ├── templates
|   |   ├── application1.yaml
|   |   └── application2.yaml
|   |   └── ...

```
The `values.yaml` file should look like the one described below:

```yaml
spec:
  destination:
    name: in-cluster
  source:
    targetRevision: HEAD
```
Files within the `templates` directory can have any name. The contents of each file should look like the one shown below:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: {{ .Values.spec.destination.name }}-application-name # concatene the variable .Values.spec.destination.name with the name of your application
  namespace: argocd
  labels: 
    cluster: {{ .Values.spec.destination.name }}
  finalizers:
  - resources-finalizer.argocd.argoproj.io
spec:
  destination:
    namespace: default
    name: {{ .Values.spec.destination.name }}
  project: default
  source:
    path: applicationpath # customize the path within the Git repository that contains your application's package.
    repoURL: https://github.com/yourusername/yourrepository # customize with the URL of your Git repository
    targetRevision: {{ .Values.spec.source.targetRevision }}
  syncPolicy:
    automated: 
      selfHeal: true
      prune: true
```
You can get a complete example of an Enforcement Core Repository [here](https://github.com/globocom/enforcement-core-example.git). 
