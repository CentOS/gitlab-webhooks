# Gitlab Webhooks

This repository contains the required resources do deploy the gitlab-webhooks app on openshift.

All images are build on top of the `centos:latest` tag.

## Project Info

|                 | Project Info                                      |
| --------------- | ------------------------------------------------- |
| License:        | MIT                                               |
| Build:          | Docker                                            |
| Issue tracker:  | https://github.com/CentOS/gitlab-webhooks/issues  |
| Mailing lists:  | [centos-devel](https://lists.centos.org/pipermail/centos-devel/) ([subscribe](https://lists.centos.org/mailman/listinfo/centos-devel)) |
| IRC:            | [#centos-stream](https://webchat.freenode.net/?channels=centos-stream) channel in the [freenode](http://freenode.net/) network. |

## Structure

* `deploy/openshift`: openshift yaml deployment files
* `deploy/ansible`: ansible playbooks for an automated installation
* `images`: linux container images files
* `images/gitlab-webhook`: webhook flask app source code
* `samples`: sample files for reference

## Deployment

NOTE: Any commands using `oc` can be replaced by `kubectl`.

Create a secret with your fedora messaging credentials:

```sh
oc \
create \
secret \
generic \
gitlab-webhook-fm-certs \
--from-file=ca.pem=$HOME/.local/certs/fedora-messaging/gitlab/ca.pem \
--from-file=cert.pem=$HOME/.local/certs/fedora-messaging/gitlab/cert.pem \
--from-file=key.pem=$HOME/.local/certs/fedora-messaging/gitlab/key.pem
```

NOTE: tehet is currently a bug in fedora-messaging where the "cert.pem" file needs to start with a blank line.

Create required resources:

```sh
oc apply -f deploy/openshift
```

You can check the status of your pod by running (should be `Running` at some point):

```sh
oc get pods -w
```

### Environment Variables

| Variable              | Default Value                                   | Description                             |
|-----------------------|-------------------------------------------------|-----------------------------------------|
| WEB_WORKERS           | 5                                               | gunicorn worker amount                  |
| LOG_LEVEL             | INFO                                            | application log level                   |
| FEDORA_MESSAGING_CONF |                                                 | fedora messaging configuration file     |
| IS_PRODUCTION         | False                                           | production environment bool flag        |
| LOGGER_NAME           | \_\_name\_\_                                    | the python logger name                  |
| GITLAB_TOKEN          |                                                 | gitlab token for request authentication |
| TOPIC_TEMPLATE        | {web_url.hostname}.{web_url.path}.{object_kind} | fedora messaging topic template         |

#### Notes

* `FEDORA_MESSAGING_CONF`: needs to be set if `IS_PRODUCTION` is set to `True`;
* `IS_PRODUCTION`: will not send a message to fedora messaging if set to `True`;
* `TOPIC_TEMPLATE`: parses the topic based on runtime vars (includes environment variables);
  * `object_kind`: received from the gitlab webhook json payload (can be mixed with static string as well);
  * `web_url`: the parsed url from the repository (includes all groups and subgroups);
  * `os.environ`: all environment variables are availabe for usage;
* `GITLAB_TOKEN`: always required, regardless of `IS_PRODUCTION` value.


Sample fedora-messaging configration file:

```toml
amqp_url = "amqps://myuser:@rabbitmq.fedoraproject.org/%2Fpubsub"

[client_properties]
app = "myuser"
 
[tls]
ca_cert = "/opt/gitlab-webhook/etc/certs/ca.pem"
certfile = "/opt/gitlab-webhook/etc/certs/cert.pem"
keyfile = "/opt/gitlab-webhook/etc/certs/key.pem"
```

## Development

Docker compose can be used for local development:

```
docker-compose up
```

The above command will run the latest image tag and expose the webhook app service in the `5000` port.

### Testing

Testing requests with curl:

```sh
# webhook request
curl -X POST -H 'X-Gitlab-Token: foobar' -H 'Content-Type:application/json'  -d @samples/gitlab/push.json  http://127.0.0.1:5000
# info request, returns basic env data
curl http://127.0.0.1:5000/info
# health request for kubernetes readinessProbe
curl http://127.0.0.1:5000/health
```

## License

```
Copyright 2020 Red Hat

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
