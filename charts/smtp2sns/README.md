# smtp2sns
[![GPL3](https://img.shields.io/github/license/smtp2sns/smtp2sns)](https://github.com/smtp2sns/smtp2sns/blob/main/LICENSE)
[![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/smtp2sns)](https://artifacthub.io/packages/search?repo=smtp2sns)


## Overview

This is a Helm chart for deploying the `smtp2sns` application, which listens for SMTP messages and forwards them to a AWS SNS server to be send SMS.

## Prerequisites

- Kubernetes (tested for 1.30+)
- Helm (tested for 3.15+)

## Add the Repository

Before installation the repository must be added.

```
helm repo add smtp2sns https://smtp2sns.github.io/smtp2sns
```

## Installing the Chart

To install the chart with the release name `smtp2sns`:

```bash
helm install smtp2sns smtp2sns/smtp2sns --set app.topic=<arn:topic> --set app.region=us-west-1
``` 

The command deploys `smtp2sns` on the Kubernetes cluster in the default configuration. 
The configuration section lists the parameters that can be configured during installation.

## Uninstalling the Chart

To uninstall/delete the `smtp2sns` deployment:

```bash
helm uninstall smtp2sns
```

The command removes all the Kubernetes components associated with the chart and deletes the release.

## Configuration

The following table lists the configurable parameters of the `smtp-gotify` chart and their default values.

| Parameter          | Description                            | Default                       |
|--------------------|----------------------------------------|-------------------------------|
| `replicaCount`     | Number of replicas                     | `1`                           |
| `image.repository` | Image repository                       | `ghcr.io/smtp2sns/smtp2sns`   |
| `image.tag`        | Image tag                              | `latest`                      |
| `image.pullPolicy` | Image pull policy                      | `IfNotPresent`                |
| `service.type`     | Service type                           | `ClusterIP`                   |
| `service.port`     | Service port                           | `1025`                        |
| `app.topic`        | AWS SNS sms topic                      | `"arn:aws:sns:us-west-1:xxxxx:MyTopic"`              |
| `app.region`       | AWS Region                             | `us-west-1`                   |
| `app.mock`         | Feature: activate mock service         | `"disabled"`                   |
| `app.secret.name`  | Kubernetes secret that stores AWS Credentials| `""`                    |
| `resources`        | CPU/Memory resource requests/limits    | `{}`                          |
| `nodeSelector`     | Node labels for pod assignment         | `{}`                          |
| `tolerations`      | Toleration labels for pod assignment   | `{}`                          |
| `affinity`         | Affinity settings for pod assignment   | `{}`                          |


**Important**: The variable `app.topic` should be in the form `arn:aws:sns:[region]:[account-id]:[topic]`.

**Important**: Do *NOT* use the variable `app.mock` in *PRODUCTION* .

Specify each parameter using the `--set key=value[,key=value]` argument to `helm install`. For example:

```bash
helm install smtp2sns smtp2sns/smtp2sns --set app.topic=<arn:topic> --set app.region=us-west-1
````

Alternatively, a YAML file that specifies the values for the parameters can be provided while installing the chart. 
For example:

```bash
helm install smtp2sns smtp2sns/smtp2sns  -f values.yaml
```

## License

This project is licensed under the GPL3.