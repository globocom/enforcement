# Enforcement
## Introduction
Enforcement is a service responsible for integrating clusters orchestrated by Rancher to ArgoCD, making it possible for the clusters to use the benefits of GitOps at the same time they are created.

Enforcement also allows you to configure a GIT repository with standard applications that must be installed on all clusters created by Rancher.

## How does it work?

The Enforcement service lists all the clusters orchestrated by Rancher through its API Rest. After obtaining all the clusters, the service configures all of them on the ArgoCD and requests the installation of the standard applications present in the configured Git repository. ArgoCD installs all applications on the configured clusters and guarantees that they will always be installed.

\
![alt text](https://raw.githubusercontent.com/globocom/enforcement-service/master/architecture.png)
