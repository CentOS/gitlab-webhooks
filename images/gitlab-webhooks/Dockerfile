FROM centos:latest

RUN yum install -y python38 python38-devel python38-pip git telnet && \
yum groupinstall -y 'Development Tools'

RUN pip3 install -U gunicorn

RUN mkdir -p \
/opt/gitlab-webhook/src \
/opt/gitlab-webhook/etc \
/opt/gitlab-webhook/etc/certs \
/opt/gitlab-webhook/fedora-messaging

COPY gitlab-webhook /opt/gitlab-webhook/src
RUN (cd /opt/gitlab-webhook/src; python3.8 setup.py install)

COPY entrypoint /opt/gitlab-webhook/bin/entrypoint

RUN chown -R 1001:root /opt/gitlab-webhook

USER 1001

ENTRYPOINT ["/opt/gitlab-webhook/bin/entrypoint"]
