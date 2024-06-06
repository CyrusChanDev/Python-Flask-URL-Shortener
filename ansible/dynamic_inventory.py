#!/usr/bin/env python3

import subprocess
import json
import os


# Change script's working directory to the script's own directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Change to the relative Terraform directory is necessary to access the state file that we will retrieve the dynamic public IPv4 address from
os.chdir("../terraform")

public_ipv4 = subprocess.check_output(["terraform output -raw ec2_instance_public_ip"], shell=True)
public_ipv4_string = public_ipv4.decode("utf-8").strip()

# Change back to original working directory
os.chdir("../ansible")


inventory = {
    "web": {
        "hosts": ["ec2-instance"],
        "vars": {
            "ansible_user": "ubuntu",
            "ansible_ssh_private_key_file": "~/PersonalProject.pem"
        }
    },
    "_meta": {
        "hostvars": {
            "ec2-instance": {
                "ansible_host": public_ipv4_string
            }
        }
    }
}

# DEBUG purposes
print(json.dumps(inventory, indent=2))
