# Packet Deploy

Simple example tool for deploying a server using packet.net's api

# Installation

Installation is simple by using pip to install the package.

```shell
git clone https://github.com/mikemrm/python-packet-deploy.git
cd python-packet-deploy
pip3 install .
pd --version
```

# Configuration

In order to use this, an api auth token and project must be provided.

You can do this two ways:

```shell
pd --auth AUTH_TOKEN --project PROJECT_ID list

# or

export PACKET_AUTH=AUTH_TOKEN PACKET_PROJECT=PROJECT_ID
pd list
```

# Usage

```shell
pd --help
usage: pd [-h] [--version] [--host HOST] [--auth AUTH] [--project PROJECT]
          [--org ORG] [--facility FACILITY] [--plan PLAN] [--os OS]
          [--hostname HOSTNAME] [--device-id DEVICE_ID]
          {list,capacity,power_up,power_down,reboot,add,remove}

These Environment variables can be used instead of arguments:
  PACKET_HOST
  PACKET_AUTH
  PACKET_PROJECT
  PACKET_ORG

positional arguments:
  {list,capacity,power_up,power_down,reboot,add,remove}

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit

API arguments:
  --host HOST           packet.net api url. Default: https://api.packet.net
  --auth AUTH           API auth token [Required]
  --project PROJECT     Project id for associated devices [Required]
  --org ORG             Organization id for associated devices

add arguments:
  --facility FACILITY   Facility code
  --plan PLAN           Plan slug
  --os OS               Operating System slug
  --hostname HOSTNAME   Hostname

power_up/power_down/reboot/remove arguments:
  --device-id DEVICE_ID
                        UUID of a device to be deleted
```

