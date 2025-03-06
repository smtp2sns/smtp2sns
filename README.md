# smtp2sns

![docker compilation workflow](https://github.com/smtp2sns/smtp2sns/actions/workflows/docker-publish.yml/badge.svg)

This project transforms smtp messages to sms using aws sns service.
```
from: xxx@xxx.xxx
to: +1xxxxxx@sms.sms
subject: sms
body:
SMS to be send.
EOF
```


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

then you can send emails using localhost:25 without credentials

## run using helm

```bash
helm install smtp-to-sns ./smtp-to-sns-chart
```

then you can send emails using this configuration:
