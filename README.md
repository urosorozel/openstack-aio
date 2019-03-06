- Disable iPXE agent fo tianocore
`<rom bar='off'/>`

- Undefine VM with nvram
`virsh undefine vm --nvram`

- Delete ironic VM
`virsh list --all --name|grep aio|grep ironic| xargs -Ixx bash -c "virsh destroy xx;virsh undefine xx"`
`virsh vol-list --pool vgdata1|grep aio|grep ironic |awk '{print $1}' | xargs -Ixx virsh vol-delete --pool vgdata1 --vol xx'`


* Issues with provisioning
- Swift tempurl not set
  Check if tempurl is set on container
  Run `swift stat` as glance user
`swift  --os-username "service:glance" --os-password "6a936307655bf51bcd3d" --os-auth-url http://172.29.236.100:5000/v3 --os-identity-api-version 3 post -m temp-url-key:c6641b0a611be09f155eb63d`
