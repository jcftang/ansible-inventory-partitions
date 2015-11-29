# Partions based inventory for Ansible

This is a very simplistic dynamic inventory for ansible. It takes
Slurm based configuration lines in the form of...


```
PartitionName=all Nodes=dev[0-5] KEY0=VALUE0
PartitionName=web Nodes=dev[0-2,5] KEY1=VALUE1
PartitionName=database Nodes=dev[4-5] Children=storage
PartitionName=storage Nodes=dev1 ansible_ssh_user=admin
```

This plugin takes the approach of partitioning up a cluster of
nodes, each partition has it's own set of variables which are not
merged with values from other partitions.

It should be possible to lift the PartitionName lines from a
slurm.conf file and feed it to this script.

The keys 'PartitionName' and 'Nodes' are required, the 'Children'
keyword is optional. All other key=value pairs are parsed as such
and added as variables to the partitions.

To use this plugin copy the partitions.py file into your ansible
playbook repository and create a partitions.conf file.

Excute the partitions.py like this...

```
./partitions.py --list
ansible all -i ./partitions.py -a uptime
```

The plugin generates this type of output...

```
{
    "all": {
        "children": [],
        "hosts": [
            "dev0",
            "dev1",
            "dev10",
            "dev11",
            "dev12",
            "dev13",
            "dev14",
            "dev15",
            "dev16",
            "dev17",
            "dev18",
            "dev19",
            "dev2",
            "dev20",
            "dev21",
            "dev22",
            "dev23",
            "dev24",
            "dev25",
            "dev3",
            "dev4",
            "dev5",
            "dev6",
            "dev7",
            "dev8",
            "dev9"
        ],
        "vars": {
            "KEY0": "VALUE0"
        }
    },
    "database": {
        "children": [
            "storage"
        ],
        "hosts": [
            "dev10",
            "dev11",
            "dev12",
            "dev13",
            "dev14",
            "dev15",
            "dev16",
            "dev17",
            "dev9"
        ],
        "vars": {}
    },
    "storage": {
        "children": [],
        "hosts": [
            "dev10",
            "dev11",
            "dev12",
            "dev13",
            "dev14",
            "dev15",
            "dev16",
            "dev17",
            "dev9"
        ],
        "vars": {
            "ansible_ssh_user": "admin"
        }
    },
    "web": {
        "children": [],
        "hosts": [
            "dev0",
            "dev1",
            "dev18",
            "dev19",
            "dev2",
            "dev20",
            "dev21",
            "dev22",
            "dev23",
            "dev24",
            "dev25",
            "dev3",
            "dev4",
            "dev5",
            "dev6",
            "dev7",
            "dev8"
        ],
        "vars": {
            "KEY1": "VALUE1"
        }
    }
}
```
