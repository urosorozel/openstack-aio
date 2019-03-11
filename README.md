### Undefine UEFI virtual machines
- Disable iPXE agent fo tianocore
`<rom bar='off'/>`

- Undefine VM with nvram
`virsh undefine vm --nvram`

### Delete ironic VM
```
virsh list --all --name|grep aio|grep ironic| xargs -Ixx bash -c "virsh destroy xx;virsh undefine xx --nvram"
virsh vol-list --pool vgdata1|grep aio|grep ironic |awk '{print $1}' | xargs -Ixx virsh vol-delete --pool vgdata1 --vol xx
```


### Issues with provisioning
- Swift tempurl not set
  Check if tempurl is set on container
  Run `swift stat` as glance user
`swift  --os-username "service:glance" --os-password "6a936307655bf51bcd3d" --os-auth-url http://172.29.236.100:5000/v3 --os-identity-api-version 3 post -m temp-url-key:c6641b0a611be09f155eb63d`

### Build virtual nodes
```
echo {1..5}| tr ' ' '\n' |xargs -Ixx -t openstack baremetal node set --driver-info ipmi_address=192.168.122.20xx QEMU_01-0c-c4-7a-bb-ff-fxx
echo {1..5}| tr ' ' '\n' |xargs -Ixx -t bash -c "openstack baremetal node manage QEMU_01-0c-c4-7a-bb-ff-fxx;openstack baremetal node provide QEMU_01-0c-c4-7a-bb-ff-fxx"
NET_IRONIC_UUID=$(openstack network list -f value | grep ironic-network | awk '{print $1}')
NET_DUMMY_UUID=$(openstack network list -f value | grep public-flat-network | awk '{print $1}')
echo {1..5}| tr ' ' '\n' |xargs -Ixx -t openstack server create --key-name osa_key  --flavor baremetal-flavor --image ubuntu-bionic  --config-drive True --nic net-id=$NET_IRONIC_UUID baremetalxx
openstack server create --key-name osa_key --flavor virtual-flavor --security-group server_ssh_icmp --image cirros-0.3.6 --nic net-id=$NET_DUMMY_UUID virtual
```
