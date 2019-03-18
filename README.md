# Openstack Ironic AIO
Collection of ansible playbooks which build Openstack Ironic AIO environment.

## How to use
1. Git clone repositoy
```
# git clone https://github.com/urosorozel/openstack-aio.git
```
2. Edit build_vars
```
# Edit and source this file if you want to create overrides
#export PROXY_SERVER=http://x.x.x.x:3128
#export NO_PROXY_SERVERS=".domain1.com,.domain2.com"
export NAME_SERVER=1.1.1.1
export DISK_POOL_NAME=data
export DISK_POOL_PATH=/data
export HOST_BRIDGE=host-aio
export IRONIC_BRIDGE=ironic-aio
# Define http server ip address where custom IPA images can be downloaded from
# By default tinyipa image is downloaded
#export IPA_IMAGE_SERVER=x.x.x.x
# Install extra cacert
#export CA_CERT="$(cat cacert.crt)"
# Deploy AIO image filename
# export AIO_IMAGE_NAME=openstack-aio.qcow2
```
4. Source variables

```
# source build_vars
```
3. Run ansible_install.sh
```
# ./ansible_install.sh
```

4. Create AIO virtual machine by running either:
```
# ./rebuild.sh
```

or

```
# ansible-playbook build_aio.yml
# ansible-playbook setup_aio.yml
```

### Environment variables

`PROXY_SERVER`  set http_proxy server if you don't have direct access to internet
`CA_CERT`  this variable should include CA certificate if mitm proxy is used
`NAME_SERVER  DNS server to be used
`DISK_POOL_NAME`  libvirt disk pool name
`DISK_POOL_PATH`  libvirt dir pool path
`HOST_BRIDGE`  libvirt host network name
`IRONIC_BRIDGE`  libvirt ironic network name
`IPA_IMAGE_SERVER`  custom IPA image http server address
`AIO_IMAGE_NAME`  if you are deploying AIO from existing image place image in DISK_POOL_PATH and provide filename

### Delete ironic VM
```
virsh list --all --name|grep aio|grep ironic \
                | xargs -Ixx bash -c "virsh destroy xx;virsh undefine xx --nvram"
virsh vol-list --pool  ${DISK_POOL_NAME:-data}| grep aio|grep ironic \
                | awk '{print $1}' | xargs -Ixx virsh vol-delete --pool ${DISK_POOL_NAME:-data} --vol xx
```


### Issues with provisioning
Swift tempurl issues, check if tempurl is set on container, run `swift stat` as glance user
```
swift  --os-username "service:glance" --os-password "6a936307655bf51bcd3d" \
                  --os-auth-url http://172.29.236.100:5000/v3 \
                  --os-identity-api-version 3 post -m temp-url-key:c6641b0a611be09f155eb63d
```

### Build virtual nodes
```
echo {1..5}| tr ' ' '\n' |xargs -Ixx -t openstack baremetal node set --driver-info \
                   ipmi_address=192.168.10.20xx QEMU_01-0c-c4-7a-bb-ff-fxx

echo {1..5}| tr ' ' '\n' |xargs -Ixx -t bash -c "openstack baremetal node manage \
                    QEMU_01-0c-c4-7a-bb-ff-fxx;openstack baremetal node provide QEMU_01-0c-c4-7a-bb-ff-fxx"

NET_IRONIC_UUID=$(openstack network list -f value | grep ironic-network | awk '{print $1}')

NET_DUMMY_UUID=$(openstack network list -f value | grep public-flat-network | awk '{print $1}')

echo {1..5}| tr ' ' '\n' |xargs -Ixx -t openstack server create --key-name osa_key \
                     --flavor baremetal-flavor --image ubuntu-bionic  --config-drive True \
                     --nic net-id=$NET_IRONIC_UUID baremetalxx

openstack server create --key-name osa_key --flavor virtual-flavor --security-group server_ssh_icmp \
                     --image cirros-0.3.6 --nic net-id=$NET_DUMMY_UUID virtual
```

### Undefine UEFI virtual machines
- Disable iPXE agent fo tianocore
`<rom bar='off'/>`

- Undefine VM with nvram
`virsh undefine vm --nvram`
