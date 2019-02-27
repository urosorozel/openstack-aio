- Disable iPXE agent fo tianocore
`<rom bar='off'/>`

- Undefine VM with nvram
`virsh undefine vm --nvram`

- Delete ironic VM
`virsh list --all --name|grep aio|grep ironic| xargs -Ixx bash -c "virsh destroy xx;virsh undefine xx"
`virsh vol-list --pool vgdata1|grep aio|grep ironic |awk '{print $1}' | xargs -Ixx virsh vol-delete --pool vgdata1 --vol xx'`
