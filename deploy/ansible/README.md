# Ansible Installer

Provisions the required webhook resource into openshift.

The only requirement is that the user running the playbooks is already logged in an openshift cluster.

## User Guide

To provision the webhook application in openshift:

```sh
ansible-playbook \
-i inventories/localhost.ini \
playbooks/install.yml
```

All available variables are located at: `inventories/localhost.ini`.

The only required var changes is around the fedora-messaging ca, cert and key files paths:

* fedora_messaging_ca_path
* fedora_messaging_cert_path
* fedora_messaging_key_path

