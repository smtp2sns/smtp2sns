# smtp2sns

![docker compilation workflow](https://github.com/smtp2sns/smtp2sns/actions/workflows/docker-publish.yml/badge.svg) ![helm release workflow](https://github.com/smtp2sns/smtp2sns/actions/workflows/helm-release.yml/badge.svg) [![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/smtp2sns)](https://artifacthub.io/packages/search?repo=smtp2sns)

This project transforms smtp messages to sms using aws sns service.
```
from: xxx@xxx.xxx
to: +1xxxxxx@sms.sms
subject: sms
body:
SMS to be send.
EOF
```
## run using docker
```bash
docker run -d --rm -p 1025:1025 -e TOPIC_ARN=arn:xxx -e AWS_REGION=us-west-1 -e AWS_ACCESS_KEY_ID=xxxx -e AWS_SECRET_ACCESS_KEY=yyyy ghcr.io/smtp2sns/smtp2sns
```


then you can send emails using localhost:1025 without credentials


## run using docker-compose
```bash
vi .env
TOPIC_ARN=arn:
AWS_REGION=us-west-1
AWS_ACCESS_KEY_ID=xxxx
AWS_SECRET_ACCESS_KEY=yyyy
```

```bash
docker compose up -d
```

then you can send emails using localhost:1025 without credentials

You can add MOCK_SERVICE if you want to mock/simulate the sms backend. Do not use it in production

## run using helm

Create a SNS to send sms obtain the topic_arn

create an AWS user in IAM that has the following permissions: `sns:Publish` to the specific topic_arn

create a secret in the cluster with those credentials:
```bash
kubectl create secret generic aws-credentials \
    --from-literal=AWS_ACCESS_KEY_ID='xxxx' \
    --from-literal=AWS_SECRET_ACCESS_KEY='yyyy' \

```
create a values.yaml file with the `topic` and the `region`:
```yaml
app:
  region: us-west-1
  # add topic arn value
  topic: arn:aws:sns:us-west-1:xxxxx:MyTopic
  # mock service (do not use in production)
  #mock: "true"  
  secret: 
    name: aws-credentials
```

```bash
helm repo add smtp2sns https://smtp2sns.github.io/smtp2sns

helm install smtp2sns smtp2sns/smtp2sns -f values.yaml
# or in local
helm install smtp2sns ./charts/smtp2sns -f values.yaml
```

then you can send emails using this configuration:
```
smtp2sns:1025
```


# test

There is a test script to localhost:1025 to test the smtp server. Netcat and bash is needed (nc)
```bash
./test.sh
```

execution example:
```bash
$ ./test.sh
220 eccc82e00c5f Python SMTP 1.4.6
250-eccc82e00c5f
250-SIZE 33554432
250-8BITMIME
250-SMTPUTF8
250 HELP
250 OK
250 OK
354 End data with <CR><LF>.<CR><LF>
250 OK: queued as mock:1234
221 Bye
```
