#!/bin/bash

function reset_vms(){
  echo "Reset all VM's"
  virsh list --name | egrep 'openstack-aio' | xargs -Ixx bash -c "virsh reset xx"
  echo "Sleeping 30sec to allow boot"
  sleep 35
}

function chech_health(){
echo "Check health..."
ansible -i environments/aio/hosts  -m ping all
if [[ $? -eq 4 ]];then
  reset_vms
  ansible -i environments/aio/hosts  -m ping all
  if [[ $? -eq 4 ]];then
     echo "Provisioning failure, exiting ..."
     exit 1
  fi
fi
}

virsh list --name --all| egrep 'openstack-aio' | xargs -Ixx bash -c "virsh destroy xx;virsh undefine xx --nvram"
virsh vol-list data |egrep 'openstack-aio' | egrep 'img|qcow' | awk '{print $1}' | xargs -Ixx  virsh vol-delete xx data
ansible-playbook -i environments/aio/hosts  build_vms.yml
echo "Sleeping 50 sec to allow boot"
sleep 50

#chech_health
ansible-playbook -vv setup_aio.yml
